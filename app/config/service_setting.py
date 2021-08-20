import os

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
    bsc_net_url: str = config_object["BINANCE"]["NetUrl"]
    bsc_net_chain_id: int = int(config_object["BINANCE"]["NetChainId"])
    account_from: str = config_object["ACCOUNT"]["AccountFrom"]
    account_from_private_key: str = config_object["ACCOUNT"]["AccountFromPrivateKey"]
    account_to: str = config_object["ACCOUNT"]["AccountTo"]

    web3 = Web3(Web3.HTTPProvider(bsc_net_url))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
