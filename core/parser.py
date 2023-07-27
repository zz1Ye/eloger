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
from web3 import Web3
from hexbytes import HexBytes

from core import ChainEnum
from config import Config
from core.item import EventLog
from utils import camel_to_snake
from utils.bucket import ConHashBucket


class Parser:
    def __init__(self, chain: ChainEnum):
        self.chain = chain.value
        self.nodes = Config().NODE[self.chain]
        self.scan = Config().SCAN[self.chain]
        self.a_bucket, self.n_bucket = ConHashBucket(), ConHashBucket()

        for api_key in self.scan.API_KEY:
            self.a_bucket.push(api_key)

        for node in self.nodes:
            self.n_bucket.push(node.API)

    def get_abi(self, address: str):
        address, api_key = address.lower(), self.a_bucket.get(address)
        abi_fpath = Config().DATA_DIR + "/abi/" + address + '.json'
        if os.path.exists(abi_fpath):
            with open(abi_fpath, 'r') as f:
                abi = json.load(f)
        else:
            abi_endpoint = self.scan.API + f"?module=contract&action=getabi&address={address}&apikey={api_key}"
            abi = json.loads(requests.get(abi_endpoint).text)

            with open(abi_fpath, 'w') as f:
                json.dump(abi, f)

        return abi

    def get_event_logs(self, tx_hash: str) -> List[EventLog]:
        w3 = Web3(Web3.HTTPProvider(
            self.n_bucket.get(tx_hash)
        ))
        receipt = w3.eth.get_transaction_receipt(HexBytes(tx_hash))

        elogs = []
        for item in receipt["logs"]:
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
                    elog.event = decoded_log['event']
                    elog.args = dict(decoded_log['args'])
                    break

            elogs.append(elog)
        return elogs



