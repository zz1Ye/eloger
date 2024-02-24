#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2023/07/26 16:50
@Author  : zzYe

"""
import hashlib


# def get_hash(raw_str: str) -> int:
#     """
#     Map strings to 2 ^ 32 numbers
#     """
#     md5_str = hashlib.md5(raw_str.encode('utf-8')).hexdigest()
#     return int(md5_str, 16)


def insert_char_at_index(string_input: str, index: int, char: str) -> str:
    return string_input[:index] + char + string_input[index:]


def find_uppercase_index(string_input: str) -> list:
    return [i for i in range(len(string_input)) if string_input[i].isupper()]


def lowercase_multi_index(string_input: str, indices: list) -> str:
    return "".join([
        string_input[i].lower() if i in indices else string_input[i] for i in range(len(string_input))
    ])


def camel_to_snake(name: str) -> str:
    idx_arr = find_uppercase_index(name)
    name = lowercase_multi_index(name, idx_arr)

    for idx in idx_arr:
        name = insert_char_at_index(name, idx, '_')

    return name
