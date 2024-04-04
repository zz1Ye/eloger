#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : trace.py
@Time   : 2024/4/4 13:57
@Author : zzYe

"""
from typing import Any

from conf import Chain
from dao import JsonDao
from spider import Spider


class TxTraceSpider(Spider):
    def __init__(self, chain: Chain, dir: str):
        super().__init__(chain, dir)

    def crawl_tx_trace(self, tx_hash: str) -> Any:
        tx_hash = tx_hash.lower()

        dao = JsonDao(f"{self.dir}/{tx_hash}.json")
        trace = dao.load()
        if trace is not None:
            return trace[0]

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "trace_transaction",
            "params": [tx_hash]
        }

        trace = self._crawl(
            url=self.node_bucket.get(tx_hash),
            method="POST",
            headers=headers,
            payload=payload,
        )
        dao.save([trace], mode='w')

        return trace









