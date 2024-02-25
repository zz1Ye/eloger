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
digger = Parser("BSC", config)
elogs = digger.get_event_logs(tx_hash)

for elog in elogs:
    print(elog)
```

When the run is complete, the event log data is saved in the `log` folder in the `data` folder. 
In addition, parsing the input field of a transaction is allowed.

```Python
input_data = parser.parse_input(tx_hash)
```
The input data is saved in the `input` folder in the `data` folder.

## 👑 Other chains

If you need to parse event logs on other chains,
you can add the relevant configuration in `config.yml` under the `config` module. 
Now take `Ethereum (ETH)` as an example.

```Python
# config.yml

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

💡 In addition, you need to ensure that the `YML format` of the added chain is correct (note the necessary `indentation`).
