#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2023/07/26 16:50
@Author  : zzYe

"""
import hashlib


def get_hash(raw_str: str) -> int:
    """
    Map strings to 2 ^ 32 numbers
    """
    md5_str = hashlib.md5(raw_str.encode('utf-8')).hexdigest()
    return int(md5_str, 16)