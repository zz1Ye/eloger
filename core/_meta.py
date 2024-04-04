#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : item.py
@Time    : 2023/07/26 18:17
@Author  : zzYe

"""

from typing import Optional
from pydantic import BaseModel


class Input(BaseModel):
    transaction_hash: str
    input: str

    function: str = None
    args: Optional[dict] = None


class EventLog(BaseModel):
    address: str
    block_hash: str
    block_number: int
    data: str
    log_index: int
    removed: bool
    topics: list
    transaction_hash: str
    transaction_index: int

    event: Optional[str] = None
    args: Optional[dict] = None



