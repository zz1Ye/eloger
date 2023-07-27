#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : test.py
@Time    : 2023/07/26 16:31
@Author  : zzYe

"""
import json

import numpy as np
import requests
from tqdm import tqdm

from core.item import ChainEnum
from core.parser import Parser
import pandas as pd

if __name__ == '__main__':
    tx_hash = "0x00129bd20219b59a008bcda102e4b93e2ff41480a473ce65055f78495cc1d3fb"
    parser = Parser(ChainEnum.ETH)
    parser.get_event_logs(tx_hash)
    exit(0)


    # Get ABI of contract
    contracts = pd.read_csv("data/decimals.csv").iloc[:, 0].tolist()
    ETHERSCAN_API_KEY = "S7N1S396ZB98XYC5WQ3IWEPDBGJKESXH5B"

    from web3 import Web3

    node_arr = [
        "https://bsc-dataseed1.ninicoin.io/",
        "https://bsc-dataseed2.ninicoin.io/",
        "https://bsc-dataseed3.ninicoin.io/"
    ]

    # 连接到以太坊网络
    w3 = Web3(Web3.HTTPProvider(node_arr[2]))

    res = []
    un_arr = []
    for contract in tqdm(contracts):
        # abi_endpoint = f"https://api.bscscan.com/api?module=contract&action=getabi&address={contract}&apikey={ETHERSCAN_API_KEY}"
        # abi = json.loads(requests.get(abi_endpoint).text)
        #
        # with open('data/abi/' + contract + '.json', 'w') as f:
        #     json.dump(abi, f)

        with open("data/abi/" + contract.lower() + ".json", 'r') as f:
            abi = json.load(f)

        # 获取decimals信息
        try:
            # 获取智能合约实例
            contract_instance = w3.eth.contract(address=w3.to_checksum_address(contract.lower()), abi=abi["result"])
            decimals = contract_instance.functions.decimals().call()
            res.append([contract, decimals])
        except Exception as e:
            un_arr.append([contract])

    pd.DataFrame(np.array(res)).to_csv("data/new_decimals.csv", sep=',', encoding='utf-8',index=False)
    pd.DataFrame(np.array(un_arr)).to_csv("data/new_un_decimals.csv", sep=',', encoding='utf-8', index=False)

    print(len(res))
    print(len(un_arr))