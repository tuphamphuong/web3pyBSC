import os
from configparser import ConfigParser

from web3 import Web3
from web3.middleware import geth_poa_middleware

config_object = ConfigParser()
config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/config.ini')
print("config_file_path ", config_file_path)
config_object.read(config_file_path)

# BSC Mainnet
bsc_mainnet_url = config_object["BINANCE"]["MainnetUrl"]
bsc_mainnet_chain_id = int(config_object["BINANCE"]["MainnetChainId"])
# BSC Testnet
bsc_testnet_url = config_object["BINANCE"]["TestnetUrl"]
bsc_testnet_chain_id = int(config_object["BINANCE"]["TestnetChainId"])

account_from_private_key = config_object["ACCOUNT"]["AccountFromPrivateKey"]

web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

acc = web3.eth.account.privateKeyToAccount(account_from_private_key)
print("acc.address ", acc.address)