#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : parser.py
@Time    : 2023/07/26 16:13
@Author  : zzYe

"""
from web3 import Web3
from core import ChainEnum


class Parser:
    def __init__(
            self, chain: ChainEnum
    ):
        self.web3 = Web3.HTTPProvider("")