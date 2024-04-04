#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : _meta.py
@Time   : 2024/4/4 13:57
@Author : zzYe

"""
import json
import os
from abc import ABC

import requests
from typing import NamedTuple, Dict, Any, Union

from conf import Chain
from utils.bucket import ConHashBucket


class CrawlParams(NamedTuple):
    url: str
    method: str
    params: Dict[str, Any]


class Spider(ABC):
    def __init__(self, chain: Chain, dir: str):
        self.chain = chain
        self.dir = dir
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        self.scan_bucket, self.node_bucket = ConHashBucket(), ConHashBucket()

        # Api key load balancing
        for api_key in self.chain.scan.keys:
            self.scan_bucket.push(api_key)

        # Node load balancing
        for node in self.chain.nodes:
            self.node_bucket.push(node.api)

    def _fetch(self, url: str, method: str, **kwargs) -> Union[bytes, Dict[Any, Any]]:
        params = {}
        payload = kwargs.pop('payload', None)
        headers = kwargs.pop('headers', None)
        if payload is not None:
            params['json'] = payload
        if headers is not None:
            params['headers'] = headers

        response = requests.request(method, url, **params)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            if method.lower() == 'post' and content_type == 'application/json':
                return response.json()
            else:
                return response.content
        else:
            response.raise_for_status()

    def _parse(self, response: Union[bytes, Dict[Any, Any]]) -> Any:
        if isinstance(response, bytes):
            try:
                json_data = json.loads(response.decode('utf-8'))
                return json_data
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON response")
        else:
            return response

    def _crawl(self, url: str, method: str, **kwargs):
        fetched_data = self._fetch(url, method, **kwargs)
        return self._parse(fetched_data)