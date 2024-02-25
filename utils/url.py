#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : url.py
@Time   : 2024/2/25 10:56
@Author : zzYe

"""
from urllib.parse import urlencode, urljoin


def join_url(base_url, params):
    base_url = base_url if base_url.endswith('/') else base_url + '/'
    query_string = urlencode(params)

    full_url = urljoin(
        base_url, '?' + query_string
    )

    return full_url
