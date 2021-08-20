import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic.tools import lru_cache
from loguru import logger
from app.config.service_setting import Settings

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)

@lru_cache()
def get_settings():
    return Settings()


@router.get("/{tx_hash}")
def get(tx_hash, settings: Settings = Depends(get_settings)):
    tx = settings.web3.eth.get_transaction(tx_hash)

    result = dict({
        "blockHash": tx["blockHash"].hex(),
        "blockNumber": tx["blockNumber"],
        # "from": tx["from"],
        "gas": tx["gas"],
        "gasPrice": tx["gasPrice"],
        "hash": tx["hash"].hex(),
        "input": tx["input"],
        "nonce": tx["nonce"],
        "to": tx["to"],
        "transactionIndex": tx["transactionIndex"],
        "value": tx["value"],
        "type": tx["type"],
        "v": tx["v"],
        "r": tx["r"].hex(),
        "s": tx["s"].hex(),
    })
    return result

@router.post("/")
def post(account_to, amount: int, settings: Settings = Depends(get_settings)):
    web3 = settings.web3

    contract_abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
    contract = settings.web3.eth.contract(address=settings.erc20_contract_address, abi=contract_abi)

    account_to = web3.toChecksumAddress(account_to)
    logger.debug(f"account_to {account_to}")
    nonce_with_pending = web3.eth.getTransactionCount(settings.account_from, "pending")
    logger.debug(f"nonce_with_pending {nonce_with_pending}")

    gas_limit = 100000
    gas_price = web3.toWei(20, 'gwei')

    token_txn = contract.functions.transfer(
        account_to,
        amount,
    ).buildTransaction({
        'chainId': settings.bsc_net_chain_id,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce_with_pending,
    })

    signed_txn = web3.eth.account.signTransaction(token_txn, settings.account_from_private_key)
    logger.debug(f"signed_txn {signed_txn}")

    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.debug(f"tx_hash {tx_hash}")

    web3.eth.waitForTransactionReceipt(tx_hash, timeout=600, poll_latency=10)
    logger.debug("Wait done")

    # Get transaction receipt
    tx = web3.eth.get_transaction_receipt(tx_hash)
    logger.debug(f"w3.eth.get_transaction_receipt {tx}")

    result = dict({
        "blockHash": tx["blockHash"].hex(),
        "blockNumber": tx["blockNumber"],
        "contractAddress": tx["contractAddress"],
        "cumulativeGasUsed": tx["cumulativeGasUsed"],
        "from": tx["from"],
        "gasUsed": tx["gasUsed"],
        "logs": tx["logs"],
        "logsBloom": tx["logsBloom"].hex(),
        "status": tx["status"],
        "to": tx["to"],
        "transactionHash": tx["transactionHash"].hex(),
        "transactionIndex": tx["transactionIndex"],
        "type": tx["type"],
    })
    return result

@router.get("/{account_address}/count")
def count_by_acc(account_address, pending, settings: Settings = Depends(get_settings)):
    count = settings.web3.eth.getTransactionCount(account_address, "pending")

    result = dict({"count": count})
    return result
