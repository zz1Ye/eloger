#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : contract.py
@Time   : 2024/4/4 13:57
@Author : zzYe

"""
from typing import Any

from conf import Chain
from dao.tool import load_and_save
from spider import Spider
from utils.url import join_url


class ABISpider(Spider):
    def __init__(self, chain: Chain, dir: str):
        super().__init__(chain, dir)

    def crawl_abi(self, address: str) -> Any:
        address = address.lower()

        @load_and_save(self.dir)
        def _crawl_abi(id: str):
            api_key = self.scan_bucket.get(address)
            url = join_url(
                self.chain.scan.api,
                {
                    "module": "contract",
                    "action": "getabi",
                    "address": address,
                    "apikey": api_key
                }
            )

            return self._crawl(
                url=url,
                method="GET"
            )

        return _crawl_abi(id=address)



