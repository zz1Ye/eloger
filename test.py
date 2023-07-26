#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : test.py
@Time    : 2023/07/26 16:31
@Author  : zzYe

"""
from core.item import ChainEnum
from core.parser import Parser

if __name__ == '__main__':
    tx_hash = "0x00129bd20219b59a008bcda102e4b93e2ff41480a473ce65055f78495cc1d3fb"
    parser = Parser(ChainEnum.ETH)
    parser.get_event_logs(tx_hash)