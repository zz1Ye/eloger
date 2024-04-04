# eloger

> 📓 This is a tool that focuses on the parsing of smart contract event logs and input data. By using the `web3` framework to obtain all event logs of a specific transaction and parse the events in the log, the complete information of the log is obtained. 


## 🔰 Install

Before you start, enter the following command in the virtual environment.

```
pip install -r requirements.txt
```

🙌 Here, the python version used in this project is `3.9.12`.


## 🧪 Parsing

The test code is in the `test.py` file of the `test` module, 
and the test content is mainly based on the `Binance Chain(BSC)` as an example. 
Part of them are as follows.

```Python
tx_hash = "0xe82d9c4362cede63f93e381700ff01b8dd28c3de2eec4b2f077b3dc2beb4f088"
parser = Parser("BSC", config)
elogs = parser.parse_event_logs(tx_hash)

for elog in elogs:
    print(elog)
```

When the run is complete, the event log data is saved in the `log` folder in the `data` folder. 
In addition, parsing the input field of a transaction is allowed.

```Python
tx_hash = "0x2f13d202c301c8c1787469310a2671c8b57837eb7a8a768df857cbc7b3ea32d8"
parser = Parser("ETH", config)
input_data = parser.parse_input(tx_hash)
print(input_data)
```
The input data is saved in the `input` folder in the `data` folder.

## 👑 Other chains

If you need to parse event logs on other chains,
you can add the relevant configuration in `_chain.yml` under the `config` module. 
Now take `Ethereum (ETH)` as an example.

```Python
# _chain.yml

# Add ETH to CHAINS
- name: "Ethereum"
  tag: "ETH"
  scan:
    api: "https://api-cn.etherscan.com/api"
    keys:
      - "7MM6JYY49WZBXSYFDPYQ3V7V3EMZWE4KJK"
  nodes:
    - api: "https://cloudflare-eth.com"
```
Where `tag` will be used as the identifier of the chain parameter in the function.
`scan` is the browser API corresponding to the chain, and there can be multiple `keys`.
`node` is the node API corresponding to the chain, and there can be multiple.

💡 Ensure correct `YML` formatting for the added chain, with proper `indentation`.
It is also recommended to provide nodes that support `trace` queries (e.g.[Chainnodes](https://www.chainnodes.org/) is free), 
otherwise, some event logs involving proxy contracts may not be parsed correctly.
