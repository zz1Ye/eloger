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
from typing import List, Union


class JsonDao:
    def __init__(self, fpath: str):
        self.path = Path(fpath)

    def save(self, data: Union[dict, List[dict]], mode: str = 'a') -> None:
        valid_modes = ['w', 'a']
        if mode not in valid_modes:
            raise ValueError(
                "Invalid mode. Use either 'w' for write (overwrite) or 'a' for append."
            )

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

        if isinstance(data, dict):
            data = [data]

        if mode == 'a':
            origin = self.load()
            if origin is None:
                origin = []

            data.extend(origin)

        with self.path.open('w', encoding='utf-8') as json_file:
            json.dump(
                data, json_file,
                ensure_ascii=False, indent=4
            )

    def load(self) -> Union[List[dict], None]:
        if not self.path.exists():
            return None

        try:
            with self.path.open('r', encoding='utf-8') as json_file:
                content = json_file.read()
                if not content.strip():
                    return None
                return json.loads(content)
        except json.JSONDecodeError as e:
            logging.error(
                f"Json file {self.path} cannot be parsed: {e}"
            )
            return None
