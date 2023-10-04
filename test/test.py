#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : test.py
@Time    : 2023/07/26 16:31
@Author  : zzYe

"""
from config import ChainEnum
from core.parser import Parser

if __name__ == '__main__':
    # BNB Test
    tx_hash = "0xe82d9c4362cede63f93e381700ff01b8dd28c3de2eec4b2f077b3dc2beb4f088"
    parser = Parser(ChainEnum.BNB)
    elogs = parser.get_event_logs(tx_hash)

    for elog in elogs:
        print(elog)

    # Polygon Test
    tx_hash = "0x92641e15f1f7ed839072e015369886f17fcd4ca31ad08f75c87d130369b6b1b5"
    parser = Parser(ChainEnum.Polygon)
    elogs = parser.get_event_logs(tx_hash)

    for elog in elogs:
        print(elog)