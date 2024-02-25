#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : digger.py
@Time    : 2023/07/26 16:13
@Author  : zzYe

"""
import json
import requests

from typing import List

from tqdm import tqdm
from web3 import Web3
from hexbytes import HexBytes

import dao
from config.config import Config, load_config
from dao import JsonDao
from digger.item import EventLog
from utils import camel_to_snake
from utils.bucket import ConHashBucket
from utils.data import hexbytes_to_str
from utils.url import join_url

import warnings
warnings.filterwarnings(action='ignore', category=Warning)


class Parser:
    def __init__(self, tag: str, config: Config):
        self.config = config
        self.chain = config.chain(tag)
        self.scan_bucket, self.node_bucket = ConHashBucket(), ConHashBucket()

        # Api key load balancing
        for api_key in self.chain.scan.keys:
            self.scan_bucket.push(api_key)

        # Node load balancing
        for node in self.chain.nodes:
            self.node_bucket.push(node.api)

    def get_abi(self, address: str) -> dict:
        address = address.lower()

        dao = JsonDao(
            self.config.ABI_DIR + '/' + address + '.json'
        )
        abi = dao.load()
        if abi is not None:
            return abi[0]

        api_key = self.scan_bucket.get(address)
        abi_endpoint = join_url(
            self.chain.scan.api,
            {
                "module": "contract",
                "action": "getabi",
                "address": address,
                "apikey": api_key
            }
        )
        abi = json.loads(requests.get(abi_endpoint).text)
        dao.save(abi, mode='w')

        return abi

    def parse_input(self, tx_hash: str) -> dict:
        tx_hash = tx_hash.lower()

        dao = JsonDao(
            self.config.INPUT_DIR + '/' + tx_hash + '.json'
        )
        input_data = dao.load()
        if input_data is not None:
            return input_data[0]
        else:
            input_data = {}

        w3 = Web3(Web3.HTTPProvider(
            self.node_bucket.get(tx_hash)
        ))
        transaction = w3.eth.get_transaction(HexBytes(tx_hash))
        transaction_input = transaction['input']

        # Parsing input data
        function_signature = transaction_input[:10]
        contract = w3.eth.contract(abi=self.get_abi(transaction['to'])["result"])
        function = contract.get_function_by_selector(function_signature)

        function_abi_entry = next(
            (
                abi for abi in contract.abi if
                abi['type'] == 'function' and abi.get('name') == function.function_identifier
            ), None)

        if function_abi_entry:
            decoded_input = contract.decode_function_input(transaction_input)

            for i, (param_name, param_value) in enumerate(zip(function_abi_entry['inputs'], decoded_input)):
                if isinstance(param_value, dict):
                    input_data[param_name['name']] = {
                        key: ('0x' + value.hex().lstrip('0') if isinstance(value, bytes) else value)
                        for key, value in param_value.items()
                    }
                else:
                    input_data[param_name['name']] = param_value
            input_data = hexbytes_to_str(input_data)
            dao.save(input_data, mode='w')

        return input_data

    def get_event_logs(self, tx_hash: str) -> List[dict]:
        tx_hash = tx_hash.lower()

        dao = JsonDao(
            self.config.LOG_DIR + '/' + tx_hash + '.json'
        )
        elogs = dao.load()
        if elogs is not None:
            return elogs
        else:
            elogs = []

        w3 = Web3(Web3.HTTPProvider(
            self.node_bucket.get(tx_hash)
        ))
        receipt = w3.eth.get_transaction_receipt(HexBytes(tx_hash))
        for item in tqdm(receipt["logs"]):
            elog_dict = {
                camel_to_snake(k): w3.to_hex(v) if isinstance(v, bytes)
                else v for k, v in dict(item).items()
            }

            elog = EventLog.model_validate(elog_dict)

            # Get abi
            abi = self.get_abi(elog.address)
            contract = w3.eth.contract(
                w3.to_checksum_address(elog.address), abi=abi["result"]
            )

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

            elogs.append(hexbytes_to_str(elog.model_dump()))
        dao.save(elogs)

        return elogs


if __name__ == '__main__':
    parser = Parser("ETH", load_config())
    print(parser.parse_input("0x2f13d202c301c8c1787469310a2671c8b57837eb7a8a768df857cbc7b3ea32d8"))
