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

web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check connection
print("w3.clientVersion ", web3.clientVersion)
print("w3.isConnected() ", web3.isConnected())
print("w3.eth.block_number ", web3.eth.block_number)

tx_hash = "0xba59be99b81a43ebce219c712d45cee60d48904b63118ef1139ed8c47574dc83"

# Get transaction
print("w3.eth.get_transaction ", web3.eth.get_transaction(tx_hash))

# Get raw transaction
print("w3.eth.get_raw_transaction ", web3.eth.get_raw_transaction(tx_hash))

web3.eth.waitForTransactionReceipt(tx_hash, timeout=600, poll_latency=10)
print("Wait done")

# Get transaction receipt
print("w3.eth.get_transaction_receipt ", web3.eth.get_transaction_receipt(tx_hash))