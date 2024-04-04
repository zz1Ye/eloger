#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : item.py
@Time    : 2023/07/26 18:17
@Author  : zzYe

"""

from typing import Optional, NamedTuple, Dict, Any
from pydantic import BaseModel


class Input(BaseModel):
    transaction_hash: str
    args: Optional[dict] = None


class EventLog(BaseModel):
    transaction_hash: str
    address: str
    block_hash: str
    block_number: int
    data: str
    log_index: int
    removed: bool
    topics: list
    transaction_index: int

    event: Optional[str] = None
    args: Optional[dict] = None


class CrawlParams(NamedTuple):
    url: str
    method: str
    params: Dict[str, Any]
