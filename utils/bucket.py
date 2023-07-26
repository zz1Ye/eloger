#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : bucket.py
@Time    : 2023/07/26 19:35
@Author  : zzYe

"""
import bisect

from abc import ABCMeta, abstractmethod

from utils import get_hash


class Bucket(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def push(self, node: str):
        pass

    @abstractmethod
    def pop(self, node: str):
        pass


class ConHashBucket(Bucket):
    """
    Consistent Hashing Bucket
    """

    def __init__(self):
        super().__init__()
        self.cache_list = []
        self.cache_node = dict()

    def get(self, source_key: str):
        key_hash = get_hash(source_key)
        index = bisect.bisect_left(self.cache_list, key_hash)
        index %= len(self.cache_list)
        return self.cache_node[
            self.cache_list[index]
        ]

    def push(self, node: str):
        node_hash = get_hash(node)
        bisect.insort(self.cache_list, node_hash)
        self.cache_node[node_hash] = node

    def pop(self, node: str):
        node_hash = get_hash(node)
        self.cache_list.remove(node_hash)
        del self.cache_node[node_hash]
