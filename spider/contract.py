#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : contract.py
@Time   : 2024/4/4 13:57
@Author : zzYe

"""
from typing import Any

from conf import Chain
from dao import JsonDao
from spider import Spider
from utils.url import join_url


class ABISpider(Spider):
    def __init__(self, chain: Chain, dir: str):
        super().__init__(chain, dir)

    def crawl_abi(self, address: str) -> Any:
        address = address.lower()

        dao = JsonDao(f"{self.dir}/{address}.json")
        abi = dao.load()
        if abi is not None:
            return abi[0]

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

        abi = self._crawl(
            url=url,
            method="GET"
        )
        dao.save([abi], mode='w')

        return abi

