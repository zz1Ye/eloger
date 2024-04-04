#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : digger.py
@Time    : 2023/07/26 16:13
@Author  : zzYe

"""
from typing import List

from tqdm import tqdm
from web3 import Web3
from hexbytes import HexBytes

from conf.core import Config
from core import EventLog, Input
from dao.tool import load_and_save
from spider.contract import ABISpider
from spider.trace import TxTraceSpider
from utils import camel_to_snake
from utils.bucket import ConHashBucket
from utils.data import hexbytes_to_str

import warnings
warnings.filterwarnings(action='ignore', category=Warning)


class Parser:
    def __init__(self, tag: str, config: Config):
        self.config = config
        self.chain = config.chainer.get(tag)
        self.scan_bucket, self.node_bucket = ConHashBucket(), ConHashBucket()

        # Api key load balancing
        for api_key in self.chain.scan.keys:
            self.scan_bucket.push(api_key)

        # Node load balancing
        for node in self.chain.nodes:
            self.node_bucket.push(node.api)

    def get_implementation_contract(self, tx_hash: str, address: str) -> str:
        spider = TxTraceSpider(self.chain, self.config.TRACE_DIR)
        trace = spider.crawl_tx_trace(tx_hash)["result"]

        try:
            implementation = next(
                t["action"]["to"].lower()
                for t in trace
                if (
                        t["action"]["callType"].lower() == "delegatecall"
                        and t["action"]["from"].lower() == address.lower()
                )
            )
        except StopIteration:
            implementation = address.lower()

        return implementation

    def parse_event_logs(self, tx_hash: str) -> List[dict]:
        tx_hash = tx_hash.lower()

        @load_and_save(dir=self.config.LOG_DIR)
        def _parse_event_logs(id: str):
            elogs = []
            w3 = Web3(Web3.HTTPProvider(
                self.node_bucket.get(id)
            ))
            receipt = w3.eth.get_transaction_receipt(HexBytes(id))
            for item in tqdm(receipt["logs"]):
                elog_dict = {
                    camel_to_snake(k): w3.to_hex(v) if isinstance(v, bytes)
                    else v for k, v in dict(item).items()
                }
                elog = EventLog.model_validate(elog_dict)

                try:
                    impl_address = self.get_implementation_contract(
                        id, elog.address.lower()
                    )
                    abi = ABISpider(self.chain, self.config.ABI_DIR).crawl_abi(impl_address)
                    contract = w3.eth.contract(
                        w3.to_checksum_address(impl_address), abi=abi["result"]
                    )

                    # Get event signature of log (first item in topics array)
                    receipt_event_signature_hex = w3.to_hex(elog.topics[0])

                    events = [e for e in contract.abi if e["type"] == "event"]
                    for event in events:
                        # Get event signature components
                        name = event["name"]
                        param_type, param_name = [], []

                        for param in event["inputs"]:
                            if "components" not in param:
                                param_type.append(param["type"])
                                param_name.append(param["name"])
                            else:
                                param_type.append(f"({','.join([p['type'] for p in param['components']])})")
                                param_name.append(f"({','.join([p['name'] for p in param['components']])})")

                        inputs = ",".join(param_type)
                        p_t = ",".join([e.lstrip('(').rstrip(')') for e in param_type]).split(",")
                        p_n = ",".join([e.lstrip('(').rstrip(')') for e in param_name]).split(",")
                        p_p = [f"{a} {b}" for a, b in zip(p_t, p_n)]

                        # Hash event signature
                        event_signature_text = f"{name}({inputs})"
                        event_signature_hex = w3.to_hex(w3.keccak(text=event_signature_text))

                        # Find match between log's event signature and ABI's event signature
                        if event_signature_hex == receipt_event_signature_hex:
                            decoded_log = dict(contract.events[event["name"]]().process_receipt(receipt)[0])
                            elog.event, elog.args = f"{name}({','.join(p_p)})", dict(decoded_log['args'])
                            break
                except Exception as e:
                    continue

                elogs.append(hexbytes_to_str(elog.model_dump()))
            return elogs

        return _parse_event_logs(id=tx_hash)

    def parse_input(self, tx_hash: str) -> dict:
        tx_hash = tx_hash.lower()

        @load_and_save(dir=self.config.INPUT_DIR)
        def _parse_input(id: str):
            w3 = Web3(Web3.HTTPProvider(
                self.node_bucket.get(id)
            ))
            transaction = w3.eth.get_transaction(HexBytes(id))
            transaction_input = transaction['input']
            input_data = Input.model_validate({
                "transaction_hash": tx_hash,
                "input": str(transaction_input),
                "function": "",
                "args": {}
            })

            # Parsing input data
            function_signature = transaction_input[:10]
            impl_address = self.get_implementation_contract(tx_hash, transaction['to'])

            abi = ABISpider(self.chain, self.config.ABI_DIR).crawl_abi(impl_address)
            contract = w3.eth.contract(w3.to_checksum_address(impl_address), abi=abi["result"])
            function = contract.get_function_by_selector(function_signature)

            function_abi_entry = next(
                (
                    abi for abi in contract.abi if
                    abi['type'] == 'function' and abi.get('name') == function.function_identifier
                ), None)

            if function_abi_entry:
                decoded_input = contract.decode_function_input(transaction_input)
                input_data.function = function.function_identifier

                args, formal_params = {}, []
                for param in function_abi_entry['inputs']:
                    param_name, param_type = param['name'], param['type']
                    param_value = decoded_input[1].get(param_name, None)

                    formal_params.append(f"{param_type} {param_name}")
                    if isinstance(param_value, bytes):
                        args[param_name] = '0x' + param_value.hex().lstrip('0')
                    else:
                        args[param_name] = param_value

                input_data.function = f"{function.function_identifier}({','.join(formal_params)})"
                input_data.args = args
                input_data = hexbytes_to_str(input_data.model_dump())
            return input_data

        return _parse_input(id=tx_hash)