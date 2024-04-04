#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : _meta.py
@Time   : 2024/4/4 13:57
@Author : zzYe

"""
from typing import NamedTuple, Dict, Any


class CrawlParams(NamedTuple):
    url: str
    method: str
    params: Dict[str, Any]
