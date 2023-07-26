#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : item.py
@Time    : 2023/07/26 18:17
@Author  : zzYe

"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ChainEnum(Enum):
    ETH = "ETH"
    BNB = "BNB"


class EventLog(BaseModel):
    tranction_hash: str
    address: str
    name: Optional[str] = None
    topics: Optional[list] = None
    data: Optional[dict] = None