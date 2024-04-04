#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : data.py
@Time   : 2024/2/24 17:49
@Author : zzYe

"""
import hashlib
from typing import Dict, Any, Union, List

from web3.datastructures import AttributeDict
from hexbytes import HexBytes


def get_hash(raw_str: str) -> int:
    """
    Map strings to 2 ^ 32 numbers
    """
    md5_str = hashlib.md5(raw_str.encode('utf-8')).hexdigest()
    return int(md5_str, 16)


def hexbytes_to_str(data: Dict[str, Any]) -> Union[Dict[str, str], List[Dict[str, str]], str]:
    if isinstance(data, AttributeDict):
        return {key: hexbytes_to_str(value) for key, value in dict(data).items()}
    if isinstance(data, dict):
        return {key: hexbytes_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [hexbytes_to_str(item) for item in data]
    elif isinstance(data, (HexBytes, bytes)):
        return data.hex()
    else:
        return str(data)
