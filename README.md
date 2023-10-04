# eloger

> 📓 This is a tool that focuses on the parsing of smart contract event logs. By using the `web3` framework to obtain all event logs of a specific transaction and parse the events in the log, the complete information of the log is obtained. 


## Install

Before you start, enter the following command in the virtual environment.

```
pip install -r requirements.txt
```

🙌 Here, the python version used in this project is `3.9.12`.


## Testing

The test code is in the test.py file of the test module, and the test content is mainly based on the `Binance Chain(BNB)` as an example. Part of them are as follows.

```Python
tx_hash = "0xe82d9c4362cede63f93e381700ff01b8dd28c3de2eec4b2f077b3dc2beb4f088"  
parser = Parser(ChainEnum.BNB)  
elogs = parser.get_event_logs(tx_hash)
```


## Other chains

If you need to parse event logs on other chains, you can add relevant configuration in the `config.py`. Now take `Ethereum(ETH)` as an example.

```Python
# config.py

# Add ETH to ChainEnum
class ChainEnum(Enum):  
    ETH = "ETH"  
    # ...

# ...

# Add ETH to SCAN dict
SCAN: dict = {  
    'ETH': Scan(  
        URL='https://cn.etherscan.com',  
        API='https://api.etherscan.io/api',  
        NAME='Etherscan', 
        API_KEY=[  
            "...",
            "..." # Your API Key 
        ]  
    ),
    # ...
}


# Add ETH to NODE dict
NODE: dict = {  
    'ETH': [  
        Node(API="...", WEIGHT=1),
        Node(API="...", WEIGHT=1),
        Node(API="...", WEIGHT=1), # Your ETH Node API
    ],  
    # ...
}

```