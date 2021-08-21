import os
from configparser import ConfigParser

from solcx import compile_source
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Solidity source code
compiled_sol = compile_source(
    '''
         pragma solidity ^0.8.4;
    
         contract Greeter {
             string public greeting;
    
             constructor() public {
                 greeting = 'Hello';
             }
    
             function setGreeting(string memory _greeting) public {
                 greeting = _greeting;
             }
    
            function greet() view public returns (string memory) {
                 return greeting;
             }
         }
     '''
)

# Retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()
print("contract_id ", contract_id)
print("contract_interface ", contract_interface)

# get bytecode / bin
bytecode = contract_interface['bin']
print("bytecode ", bytecode)

# get abi
abi = contract_interface['abi']
print("abi ", abi)

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

my_metamask_private_key = config_object["ACCOUNT"]["AccountFromPrivateKey"]

web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))
# TODO: Disable this cause w3.eth.get_block throw exception with ... POA ... message
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check connection
print("w3.clientVersion ", web3.clientVersion)
print("w3.isConnected() ", web3.isConnected())
print("w3.eth.block_number ", web3.eth.block_number)

# Create account from private key
acc = web3.eth.account.from_key(my_metamask_private_key)
print("acc tyoe ", type(acc))
acc_checksum = web3.toChecksumAddress(acc.address)
print("web3.toChecksumAddress ", acc_checksum)

# Set default acc to use in transact
web3.eth.default_account = acc_checksum
# print("w3.eth.defaultAccount.address ", web3.eth.defaultAccount.address)
print("web3.eth.getBalance ", web3.eth.getBalance(acc.address))

Greeter = web3.eth.contract(abi=abi, bytecode=bytecode)
print("contract.address ", Greeter.address)

tx = Greeter.constructor().buildTransaction({
    'chainId': bsc_testnet_chain_id,
    'gas': 1000000,
    'gasPrice': web3.toWei(20, 'gwei'),
    'nonce': web3.eth.getTransactionCount(acc.address, 'pending'),
})
signed = web3.eth.account.signTransaction(tx, my_metamask_private_key)
tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
print(f"Contract deployed; {tx_hash.hex()} Waiting to transaction receipt")

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("tx_receipt ", tx_receipt)
print("tx_receipt.contractAddress ", tx_receipt.contractAddress)

# Call set function in smart contract
greeter = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print("greeter.functions.greet().call() ", greeter.functions.greet().call())
# TODO: Solution 1
tx = Greeter.functions.setGreeting('Nihao').buildTransaction({
    'chainId': bsc_testnet_chain_id,
    'gas': 100000,
    'gasPrice': web3.toWei(160, 'gwei'),
    'nonce': web3.eth.getTransactionCount(acc.address, 'pending'),
    # TODO: 'to' required?
    'to': acc_checksum,
})
signed = web3.eth.account.signTransaction(tx, my_metamask_private_key)
tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
print(f"Function called: {tx_hash.hex()} Waiting to transaction receipt")

greeter = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print("greeter.functions.greet().call() ", greeter.functions.greet().call())

