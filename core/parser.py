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
from web3 import Web3
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

    def get_event_logs(self, tx_hash: str):
        w3 = Web3(Web3.HTTPProvider(
            self.n_bucket.get(tx_hash)
        ))
        receipt = w3.eth.get_transaction_receipt(tx_hash)

        for elog in receipt["logs"]:
            elog_dict = {
                camel_to_snake(k): w3.to_hex(v) if isinstance(v, bytes)
                else v for k, v in dict(elog).items()
            }

            elog_item = EventLog.model_validate(elog_dict)
            elog_item.topics = [
                w3.to_hex(val) for val in elog_item.topics
            ]

            print(elog_item)

            # Get abi
            abi = self.get_abi(elog_dict.address)
            print(abi)



