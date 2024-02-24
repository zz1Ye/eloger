#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : config.py
@Time   : 2024/2/24 16:25
@Author : zzYe

"""
import os
import yaml
import logging

from typing import List, Dict, Union, Any
from pydantic_settings import BaseSettings

logging.basicConfig(
    level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s'
)


class Config(BaseSettings):
    PROJECT: str = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR: str = PROJECT + "/data"
    ABI_DIR: str = DATA_DIR + "/abi"
    CHAINS: List


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
    print(load_config())