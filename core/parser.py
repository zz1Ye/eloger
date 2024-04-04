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
from dao import JsonDao
from core import EventLog, Input
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
        implementation = address.lower()

        spider = TxTraceSpider(self.chain, self.config.TRACE_DIR)
        trace = spider.crawl_tx_trace(tx_hash)["result"]

        for t in trace:
            action = t["action"]
            if action["callType"].lower() == "delegatecall":
                if action["from"].lower() == address.lower():
                    implementation = action["to"].lower()
                    break

        return implementation

    def parse_input(self, tx_hash: str) -> dict:
        tx_hash = tx_hash.lower()

        dao = JsonDao(
            self.config.INPUT_DIR + '/' + tx_hash + '.json'
        )
        input_data = dao.load()
        if input_data is not None:
            return input_data[0]
        else:
            input_data = Input.model_validate({
                "transaction_hash": tx_hash,
                "args": {}
            })

        w3 = Web3(Web3.HTTPProvider(
            self.node_bucket.get(tx_hash)
        ))
        transaction = w3.eth.get_transaction(HexBytes(tx_hash))
        transaction_input = transaction['input']

        # Parsing input data
        function_signature = transaction_input[:10]
        tmp_addr = transaction['to']
        if str(tmp_addr).lower() == "0xeF4fB24aD0916217251F553c0596F8Edc630EB66".lower():
            tmp_addr = "0x7Ec2E51A9c4f088354aD8Ad8703C12D81BF21677".lower()

        impl_address = self.get_implementation_contract(
            tx_hash, tmp_addr
        )
        abi = ABISpider(self.chain, self.config.ABI_DIR).crawl_abi(impl_address)
        contract = w3.eth.contract(abi=abi["result"])
        # contract = w3.eth.contract(abi=self.get_abi(transaction['to'])["result"])
        function = contract.get_function_by_selector(function_signature)

        function_abi_entry = next(
            (
                abi for abi in contract.abi if
                abi['type'] == 'function' and abi.get('name') == function.function_identifier
            ), None)

        if function_abi_entry:
            decoded_input = contract.decode_function_input(transaction_input)

            args = {}
            for i, (param_name, param_value) in enumerate(zip(function_abi_entry['inputs'], decoded_input)):
                if isinstance(param_value, dict):
                    args[param_name['name']] = {
                        key: ('0x' + value.hex().lstrip('0') if isinstance(value, bytes) else value)
                        for key, value in param_value.items()
                    }
                else:
                    args[param_name['name']] = param_value
            input_data.args = args
            input_data = hexbytes_to_str(input_data.model_dump())
            dao.save(input_data, mode='w')

        return input_data

    def parse_event_logs(self, tx_hash: str) -> List[dict]:
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
            try:
                impl_address = self.get_implementation_contract(
                    tx_hash, elog.address.lower()
                )
                abi = ABISpider(self.chain, self.config.ABI_DIR).crawl_abi(impl_address)
                # abi = self.get_abi(impl_address)

                contract = w3.eth.contract(
                    w3.to_checksum_address(impl_address), abi=abi["result"]
                )

                # Get event signature of log (first item in topics array)
                receipt_event_signature_hex = w3.to_hex(elog.topics[0])

                # Find events
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

                    # inputs = ",".join([param["type"] for param in event["inputs"]])
                    inputs = ",".join(param_type)

                    p_t = ",".join(param_type).split(",")
                    p_n = ",".join(param_name).split(",")

                    p_p = [f"{a} {b}" for a, b in zip(p_t, p_n)]

                    # Hash event signature
                    event_signature_text = f"{name}({inputs})"
                    event_signature_hex = w3.to_hex(w3.keccak(text=event_signature_text))
                    # if name.lower() == "XCalled".lower():
                    #     print(name, inputs)
                    #     print(event_signature_hex, receipt_event_signature_hex)
                    #     exit(0)

                    # Find match between log's event signature and ABI's event signature
                    if event_signature_hex == receipt_event_signature_hex:
                        decoded_log = dict(contract.events[event["name"]]().process_receipt(receipt)[0])
                        elog.event, elog.args = f"{name}({','.join(p_p)})", dict(decoded_log['args'])
                        break
            except Exception as e:
                continue

            elogs.append(hexbytes_to_str(elog.model_dump()))
        dao.save(elogs)

        return elogs


if __name__ == '__main__':
    cof = Config()
    parser = Parser(tag="ETH", config=cof)
    print(parser.parse_event_logs("0xde06f7f44b8387dc8d315081c1681943df6e2670bb30b11a5e2c2738134a1c1a"))