#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""       
@File   : dao.py
@Time   : 2024/2/24 18:57
@Author : zzYe

"""
import json
import logging
from pathlib import Path


class JsonDao:
    def __init__(self, fpath: str):
        self.path = Path(fpath)

    def save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

        with self.path.open('w', encoding='utf-8') as json_file:
            json.dump(
                data, json_file,
                ensure_ascii=False, indent=4
            )

    def load(self) -> dict:
        if not self.path.exists():
            return {}

        try:
            with self.path.open('r', encoding='utf-8') as json_file:
                return json.load(json_file)
        except json.JSONDecodeError as e:
            logging.error(
                f"Json file {self.path} cannot be parsed: {e}"
            )
            return {}

    def update(self, key: str, value) -> bool:
        data = self.load()
        if data is None or key not in data:
            return False

        data[key] = value
        self.save(data)
        return True
