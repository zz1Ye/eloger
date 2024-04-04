#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : tool.py
@Time   : 2024/4/4 16:26
@Author : zzYe

"""
from dao import JsonDao


def load_and_save(dir: str):
    fpath = f"{dir}/{{id}}.json"

    def decorator(func):
        def wrapper(*args, **kwargs):
            if "id" not in kwargs:
                return None

            id = kwargs["id"]
            dao = JsonDao(fpath.format(id=id))

            data = dao.load()
            if data is not None:
                res = data[0]
            else:
                res = func(*args, **kwargs)

            dao.save([res], mode='w')
            return res

        return wrapper

    return decorator
