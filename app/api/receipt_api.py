import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic.tools import lru_cache

from app.config.service_setting import Settings

router = APIRouter(
    prefix="/receipts",
    tags=["receipts"],
)


@lru_cache()
def get_settings():
    return Settings()


@router.get("/{tx_hash}")
def get(tx_hash, settings: Settings = Depends(get_settings)):
    tx = settings.web3.eth.get_transaction_receipt(tx_hash)
    print("tx ", tx)

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
