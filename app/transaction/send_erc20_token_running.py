import json
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
# TODO: Disable this cause w3.eth.get_block throw exception with ... POA ... message
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check connection
print("w3.clientVersion ", web3.clientVersion)
print("w3.isConnected() ", web3.isConnected())
print("w3.eth.block_number ", web3.eth.block_number)

# Get account balance
# Account From BSC Testnet
account_from = config_object["ACCOUNT"]["AccountFrom"]
print("account_from ", account_from, "web3.isChecksumAddress ", web3.isChecksumAddress(account_from))
account_from_private_key = config_object["ACCOUNT"]["AccountFromPrivateKey"]

account_from_account_balance = web3.eth.get_balance(account_from)
print("w3.eth.get_balance(account_from) ", account_from_account_balance)

# Account To BSC Testnet
account_to = config_object["ACCOUNT"]["AccountTo"]
print("account_to ", account_to, "web3.isChecksumAddress ", web3.isChecksumAddress(account_to))
account_to_private_key = config_object["ACCOUNT"]["AccountToPrivateKey"]

account_to_account_balance = web3.eth.get_balance(account_to)
print("w3.eth.get_balance(account_to) ", account_to_account_balance)

# Lord
contract_address = '0x03B8DBbc51CdF9234C24fE0328e273F2E59c6ab9' #be sure to use a BSC Address in uppercase format like this 0x9F0818B...
abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')

contract = web3.eth.contract(address=contract_address, abi=abi)

contract_total_supply = contract.functions.totalSupply().call()
print("totalSupply ", contract_total_supply)

contract_name = contract.functions.name().call()
print("contract_name ", contract_name)

contract_symbol = contract.functions.symbol().call()
print("contract_symbol ", contract_symbol)

my_metamask_contract_balance = contract.functions.balanceOf(account_from).call()
print("my_metamask_contract_balance ", my_metamask_contract_balance)

my_binance_contract_balance = contract.functions.balanceOf(account_to).call()
print("my_binance_contract_balance ", my_binance_contract_balance)

send_amount = 1000
# TODO: Nonce return lag? Workaround by pending flag
nonce = web3.eth.getTransactionCount(account_from)
print("nonce before transaction", nonce)
nonce_with_pending = web3.eth.getTransactionCount(account_from, "pending")
print("nonce with pending before transaction", nonce_with_pending)

# TODO: Choose the best limit
# TODO: Wrong solution with web3.eth.getBlock("latest").gasLimit = 30000000
# block = web3.eth.getBlock("latest")
# gasLimit = block.gasLimit
gasLimit = 100000
print("gasLimit ", gasLimit)

# TODO: Choose the best price
# gas_price = int(web3.eth.gasPrice * 1.40)
gas_price = web3.toWei(20, 'gwei')
print("gas_price ", gas_price)

token_txn = contract.functions.transfer(
     account_to,
     send_amount,
 ).buildTransaction({
     'chainId': bsc_testnet_chain_id,
     'gas': gasLimit,
     'gasPrice': gas_price,
     'nonce': nonce_with_pending,
 })
print("token_txn ", token_txn)

signed_txn = web3.eth.account.signTransaction(token_txn, account_from_private_key)
print("signed_txn ", signed_txn)

tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print("tx_hash ", tx_hash.hex())

nonce_with_pending = web3.eth.getTransactionCount(account_from, "pending")
print("nonce with pending before transaction", nonce_with_pending)

# web3.eth.waitForTransactionReceipt(tx_hash, timeout=600, poll_latency=10)
# print("Wait done")

# Get transaction
# print("w3.eth.get_transaction ", web3.eth.get_transaction(send_raw_txn_result))

# Get transaction receipt
print("w3.eth.get_transaction_receipt ", web3.eth.get_transaction_receipt(tx_hash))