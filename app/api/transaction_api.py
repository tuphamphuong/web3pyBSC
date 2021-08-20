import json
import pprint

from fastapi import APIRouter, Depends, HTTPException
from pydantic.tools import lru_cache

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

@router.get("/{account_address}/count")
def count_by_acc(account_address, pending, settings: Settings = Depends(get_settings)):
    count = settings.web3.eth.getTransactionCount(account_address, "pending")

    result = dict({"count": count})
    return result
