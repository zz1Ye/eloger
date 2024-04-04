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
from typing import Union, Any

from conf import Chainer

logging.basicConfig(
    level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s'
)
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))


class Config(BaseModel):
    PROJECT: str = ROOT_DIR
    DATA_DIR: str = PROJECT + "/data"
    ABI_DIR: str = DATA_DIR + "/abi"
    TRACE_DIR: str = DATA_DIR + "/trace"
    LOG_DIR: str = DATA_DIR + "/log"
    INPUT_DIR: str = DATA_DIR + "/input"

    chainer: Chainer = None

    def __init__(self):
        super().__init__()

        chains = load_config(f"{CUR_DIR}/_chain.yml")
        self.chainer = Chainer(**chains) if chains is not None else None


def load_config(fpath: str) -> Union[Any, None]:
    try:
        with open(fpath, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        logging.error(
            f"The file {fpath} was not found."
        )
    except yaml.YAMLError as e:
        logging.error(
            f"An error occurred while parsing file {fpath}: {e}"
        )
    return None
