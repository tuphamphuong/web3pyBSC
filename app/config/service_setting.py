import os

from loguru import logger
from pydantic import BaseSettings
from configparser import ConfigParser

from web3 import Web3
from web3.middleware import geth_poa_middleware

config_object = ConfigParser()
config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/config.ini')
print("config_file_path ", config_file_path)
config_object.read(config_file_path)


class Settings(BaseSettings):
    app_name: str = "Binance Gateway Service"
    logger.debug(f"app_name {app_name}")

    bsc_net_url: str = config_object["BINANCE"]["NetUrl"]
    logger.debug(f"bsc_net_url {bsc_net_url}")
    bsc_net_chain_id: int = int(config_object["BINANCE"]["NetChainId"])
    logger.debug(f"bsc_net_chain_id {bsc_net_chain_id}")

    web3 = Web3(Web3.HTTPProvider(bsc_net_url))
    logger.debug(f"isConnected {web3.isConnected()}")
    # TODO: Disable this cause w3.eth.get_block throw exception with ... POA ... message
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    account_from: str = web3.toChecksumAddress(config_object["ACCOUNT"]["AccountFrom"])
    logger.debug(f"account_from {account_from}")
    account_from_private_key: str = config_object["ACCOUNT"]["AccountFromPrivateKey"]
    logger.debug(f"account_from_private_key {account_from_private_key}")

    account_to: str = web3.toChecksumAddress(config_object["ACCOUNT"]["AccountTo"])
    logger.debug(f"account_to {account_to}")

    erc20_contract_address: str = web3.toChecksumAddress(config_object["CONTRACT"]["erc20_contract_address"])
    logger.debug(f"erc20_contract_address {erc20_contract_address}")
    erc20_contract_abi: str = config_object["CONTRACT"]["erc20_contract_abi"]
    logger.debug(f"erc20_contract_abi {erc20_contract_abi}")


