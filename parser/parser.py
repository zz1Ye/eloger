#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : parser.py
@Time    : 2023/07/26 16:13
@Author  : zzYe

"""
import os
import json
import requests

from typing import List

from tqdm import tqdm
from web3 import Web3
from hexbytes import HexBytes

from config import ChainEnum
from config import Config
from parser.item import EventLog
from utils import camel_to_snake
from utils.bucket import ConHashBucket

import warnings
warnings.filterwarnings(action='ignore', category=Warning)


class Parser:
    def __init__(self, chain: ChainEnum):
        self.chain = chain.value
        self.nodes = Config().NODE[self.chain]
        self.scan = Config().SCAN[self.chain]
        self.a_bucket, self.n_bucket = ConHashBucket(), ConHashBucket()

        # Api_key load balancing
        for api_key in self.scan.API_KEY:
            self.a_bucket.push(api_key)

        # Node load balancing
        for node in self.nodes:
            self.n_bucket.push(node.API)

    def get_abi(self, address: str) -> dict:
        address, api_key = address.lower(), self.a_bucket.get(address)
        if not os.path.exists(Config().ABI_DIR):
            os.makedirs(Config().ABI_DIR)

        abi_fpath = Config().ABI_DIR + '/' + address + '.json'
        if os.path.exists(abi_fpath):
            with open(abi_fpath, 'r') as f:
                abi = json.load(f)
        else:
            abi_endpoint = self.scan.API + f"?module=contract&action=getabi&address={address}&apikey={api_key}"
            abi = json.loads(requests.get(abi_endpoint).text)

            with open(abi_fpath, 'w') as f:
                json.dump(abi, f)

        return abi

    def parse_input(self, tx_hash: str):
        w3 = Web3(Web3.HTTPProvider(
            self.n_bucket.get(tx_hash)
        ))
        transaction = w3.eth.get_transaction(tx_hash)
        transaction_input = transaction['input']

        # 解析交易的input字段
        function_signature = transaction_input[:10]  # 函数签名是前10个字符
        contract = w3.eth.contract(abi=self.get_abi("0x609c690e8F7D68a59885c9132e812eEbDaAf0c9e")["result"])
        # 打印所有函数名
        for function in contract.abi:
            if function['type'] == 'function':
                print('函数名:', function['name'])
        function = contract.get_function_by_selector(function_signature)

        # 找到对应函数的ABI描述
        function_abi_entry = next(
            (abi for abi in contract.abi if abi['type'] == 'function' and abi.get('name') == 'swapAndBridge'),
            None)

        if function_abi_entry:
            # 解码函数输入参数
            decoded_input = contract.decode_function_input(transaction_input)

            for i, (param_name, param_value) in enumerate(zip(function_abi_entry['inputs'], decoded_input)):
                print(f"Parameter {i + 1}: {param_name['name']} = {param_value}")
                if isinstance(param_value, dict):  # 判断变量是否为字典类型
                    print({key: ('0x' + value.hex().lstrip('0') if isinstance(value, bytes) else value)
                           for key, value in param_value.items()})
        else:
            print("Function ABI not found")

    def get_event_logs(self, tx_hash: str) -> List[EventLog]:
        w3 = Web3(Web3.HTTPProvider(
            self.n_bucket.get(tx_hash)
        ))
        receipt = w3.eth.get_transaction_receipt(HexBytes(tx_hash))

        elogs = []
        for item in tqdm(receipt["logs"]):
            elog_dict = {
                camel_to_snake(k): w3.to_hex(v) if isinstance(v, bytes)
                else v for k, v in dict(item).items()
            }

            elog = EventLog.model_validate(elog_dict)

            # Get abi
            abi = self.get_abi(elog.address)
            contract = w3.eth.contract(w3.to_checksum_address(elog.address), abi=abi["result"])

            # Get event signature of log (first item in topics array)
            receipt_event_signature_hex = w3.to_hex(elog.topics[0])

            # Find events
            events = [e for e in contract.abi if e["type"] == "event"]
            for event in events:
                # Get event signature components
                name = event["name"]
                inputs = ",".join([param["type"] for param in event["inputs"]])
                # Hash event signature
                event_signature_text = f"{name}({inputs})"
                event_signature_hex = w3.to_hex(w3.keccak(text=event_signature_text))

                # Find match between log's event signature and ABI's event signature
                if event_signature_hex == receipt_event_signature_hex:
                    decoded_log = dict(contract.events[event["name"]]().process_receipt(receipt)[0])
                    elog.event, elog.args = decoded_log['event'], dict(decoded_log['args'])
                    break

            elogs.append(elog)
        return elogs
