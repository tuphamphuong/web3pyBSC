from fastapi import APIRouter, Depends, HTTPException
from pydantic.tools import lru_cache

from app.config.service_setting import Settings

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@lru_cache()
def get_settings():
    return Settings()


@router.get("/")
def get(private_key: str, settings: Settings = Depends(get_settings)):
    acc = settings.web3.eth.account.privateKeyToAccount(private_key)

    result = dict({
        "address": acc.address,
    })
    return result
