#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : trace.py
@Time   : 2024/4/4 13:57
@Author : zzYe

"""
from typing import Any

from conf import Chain
from spider import Spider


class TxTraceSpider(Spider):
    def __init__(self, chain: Chain):
        super().__init__(chain)

    def crawl_tx_trace(self, tx_hash: str) -> Any:
        tx_hash = tx_hash.lower()

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

        return self._crawl(
            url=self.node_bucket.get(tx_hash),
            method="POST",
            headers=headers,
            payload=payload,
        )








