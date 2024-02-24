#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : config1.py
@Time   : 2024/2/24 16:25
@Author : zzYe

"""
import os
import yaml
import logging

from pydantic import BaseModel
from typing import List, Dict, Union
from pydantic_settings import BaseSettings


logging.basicConfig(
    level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s'
)


class Chain(BaseModel):
    name: str
    tag: str
    scan: Dict
    nodes: List[Dict]


class Config(BaseSettings):
    PROJECT: str = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR: str = PROJECT + "/data"
    ABI_DIR: str = DATA_DIR + "/abi"
    LOG_DIR: str = DATA_DIR + "/log"
    INPUT_DIR: str = DATA_DIR + "/input"
    CHAINS: List[Chain]

    def chain(self, tag: str = "ETH") -> Union[Dict, None]:
        for chain in self.CHAINS:
            if chain.tag.lower() == tag.lower():
                return chain


def load_config(fpath: str = "config.yml") -> Union[Config, None]:
    try:
        with open(fpath, 'r') as file:
            data = yaml.safe_load(file)
            return Config(**data)
    except FileNotFoundError:
        logging.error(
            f"The file {fpath} was not found."
        )
    except yaml.YAMLError as e:
        logging.error(
            f"An error occurred while parsing file {fpath}: {e}"
        )


if __name__ == '__main__':
    print(load_config().chain("eth"))