#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : data.py
@Time   : 2024/2/24 17:49
@Author : zzYe

"""
import hashlib


def get_hash(raw_str: str) -> int:
    """
    Map strings to 2 ^ 32 numbers
    """
    md5_str = hashlib.md5(raw_str.encode('utf-8')).hexdigest()
    return int(md5_str, 16)
