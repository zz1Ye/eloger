#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : config.py.py
@Time    : 2023/07/26 16:17
@Author  : zzYe

"""

import os

from pydantic_settings import BaseSettings


class Scan(BaseSettings):
    URL: str
    API: str
    NAME: str
    API_KEY: list


class Node(BaseSettings):
    API: str
    WEIGHT: int


class Config(BaseSettings):
    PROJECT: str = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR: str = PROJECT + "/data"

    SCAN: dict = {
        'ETH': Scan(
            URL='https://cn.etherscan.com/',
            API='https://api.etherscan.io/api/',
            NAME='Etherscan',
            API_KEY=[
                "JCP5B6U5RXI5I7WRC19AZEZPZ21395IJSG",
                "1ICNJCWUMGGHWIT9XE3RGU7KKVY7CHSZ3T",
                "X13EN3W2FERMMVZAENUSVP4DNKTHTXD519"
            ]
        ),
        'BNB': Scan(
            URL='https://bscscan.com/',
            API='https://api.bscscan.com/api/',
            NAME='Bscscan',
            API_KEY=[
                "S7N1S396ZB98XYC5WQ3IWEPDBGJKESXH5B",
                "EGAQYID9BS2H4YC3WJITVZTXDHYSWIUJDS",
                "5H91KBTSSDGWIKDMGMGDY1RXNE4AA136UH"
            ]
        ),
    }

    NODE: dict = {
        'ETH': [
            Node(API="https://eth-mainnet.alchemyapi.io/v2/AgKT8OzbNsYnul856tenwnsnL3Pm7WRB", WEIGHT=1),
            Node(API="https://eth-mainnet.alchemyapi.io/v2/UOD8HE4CVqEiDY5E_9XbKDFqYZzJE3XP", WEIGHT=1),
            Node(API="https://eth-mainnet.alchemyapi.io/v2/gwlaWGMm1YWliQTvWtEHcjjfNXQ3W0lK", WEIGHT=1)
        ]
    }

    REQUEST_HEADERS: dict = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3',
    }