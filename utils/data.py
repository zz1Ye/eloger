#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : data.py
@Time   : 2024/2/24 17:49
@Author : zzYe

"""
import hashlib
from typing import Dict, Any, Union, List

from hexbytes import HexBytes


def get_hash(raw_str: str) -> int:
    """
    Map strings to 2 ^ 32 numbers
    """
    md5_str = hashlib.md5(raw_str.encode('utf-8')).hexdigest()
    return int(md5_str, 16)


def hexbytes_to_str(data: Dict[str, Any]) -> Union[dict, list[dict[str, str]], str]:
    if isinstance(data, dict):
        return {key: hexbytes_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [hexbytes_to_str(item) for item in data]
    elif isinstance(data, HexBytes):
        return data.hex()
    elif isinstance(data, bytes):
        return data.hex()
    else:
        return f"{data}"
