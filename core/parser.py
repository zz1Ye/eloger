#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : parser.py
@Time    : 2023/07/26 16:13
@Author  : zzYe

"""
from web3 import Web3
from core import ChainEnum
from config import Config
from utils import camel_to_snake
from utils.bucket import ConHashBucket


class Parser:
    def __init__(self, chain: ChainEnum):
        self.chain = chain.value
        self.nodes = Config().NODE[chain.value]
        self.bucket = ConHashBucket()

        for node in self.nodes:
            self.bucket.push(node.API)

    def get_event_logs(self, tx_hash: str):
        w3 = Web3(Web3.HTTPProvider(
            self.bucket.get(tx_hash)
        ))
        receipt = w3.eth.get_transaction_receipt(tx_hash)

        for log in receipt["logs"]:
            log_dict = {
                k: w3.to_hex(v) if isinstance(v, bytes)
                else v for k, v in dict(log).items()
            }
            for key, value in log_dict.items():
                print(f"{camel_to_snake(key)} type: {type(value)}")
            exit(0)


