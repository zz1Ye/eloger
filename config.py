#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : config.py.py
@Time    : 2023/07/26 16:17
@Author  : zzYe

"""

import os
from enum import Enum

from pydantic_settings import BaseSettings


class ChainEnum(Enum):
    BNB = "BNB"
    Polygon = "Polygon"


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
    ABI_DIR: str = DATA_DIR + "/abi"

    SCAN: dict = {
        'BNB': Scan(
            URL='https://bscscan.com',
            API='https://api.bscscan.com/api',
            NAME='Bscscan',
            API_KEY=[
                "S7N1S396ZB98XYC5WQ3IWEPDBGJKESXH5B",
                "EGAQYID9BS2H4YC3WJITVZTXDHYSWIUJDS",
            ]
        ),
        'Polygon': Scan(
            URL='https://polygonscan.com//',
            API='https://api.polygonscan.com/api/',
            NAME='PolygonScan',
            API_KEY=[
                "7BTFI86WFGAAD91X2AGSF7YWBWC3M4R39S",
            ]
        ),
    }

    NODE: dict = {
        'BNB': [
            Node(API="https://bsc-dataseed1.ninicoin.io/", WEIGHT=1),
            Node(API="https://bsc-dataseed2.ninicoin.io/", WEIGHT=1),
            Node(API="https://bsc-dataseed3.ninicoin.io/", WEIGHT=1),
            Node(API="https://bsc-dataseed4.ninicoin.io/", WEIGHT=1),
            Node(API="https://bsc-dataseed1.defibit.io/", WEIGHT=1),
            Node(API="https://bsc-dataseed2.defibit.io/", WEIGHT=1),
            Node(API="https://bsc-dataseed3.defibit.io/", WEIGHT=1),
            Node(API="https://bsc-dataseed4.defibit.io/", WEIGHT=1),
        ],
        'Polygon': [
            Node(API="https://rpc-mainnet.maticvigil.com", WEIGHT=1),
            Node(API="https://polygon-rpc.com", WEIGHT=1)
        ]
    }