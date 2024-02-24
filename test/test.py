#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : test.py
@Time    : 2023/07/26 16:31
@Author  : zzYe

"""
from config.config import load_config
from digger import Parser

if __name__ == '__main__':
    # # BNB Test
    # tx_hash = "0xe82d9c4362cede63f93e381700ff01b8dd28c3de2eec4b2f077b3dc2beb4f088"
    # digger = Parser(ChainEnum.BNB)
    # elogs = digger.get_event_logs(tx_hash)
    #
    # for elog in elogs:
    #     print(elog)
    #
    # # Polygon Test
    # tx_hash = "0x92641e15f1f7ed839072e015369886f17fcd4ca31ad08f75c87d130369b6b1b5"
    # digger = Parser(ChainEnum.Polygon)
    # elogs = digger.get_event_logs(tx_hash)
    #
    # for elog in elogs:
    #     print(elog)

    # ETH Test
    tx_hash = "0x2f13d202c301c8c1787469310a2671c8b57837eb7a8a768df857cbc7b3ea32d8"
    parser = Parser(load_config().chain("eth"))
    elogs = parser.parse_input(tx_hash)

    # for elog in elogs:
    #     print(elog)