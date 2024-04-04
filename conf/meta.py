#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : meta.py
@Time   : 2024/4/4 11:28
@Author : zzYe

"""
from typing import List, Optional
from pydantic import BaseModel


class Scan(BaseModel):
    api: str
    keys: List[str]


class Node(BaseModel):
    api: str


class Chain(BaseModel):
    name: str
    tag: str
    scan: Scan
    nodes: List[Node]


class Chainer(BaseModel):
    chains: List[Chain]

    def get(self, tag: str = "ETH") -> Optional[Chain]:
        chain = next(
            (
                c
                for c in self.chains
                if c.tag.lower() == tag.lower()
            ), None
        )
        return chain
