from fastapi import APIRouter, Depends, HTTPException
from pydantic.tools import lru_cache

from app.config.service_setting import Settings

router = APIRouter(
    prefix="/gases",
    tags=["gases"],
)


@lru_cache()
def get_settings():
    return Settings()


@router.get("/")
def get_gas(settings: Settings = Depends(get_settings)):
    block = settings.web3.eth.getBlock("latest")

    result = dict({
        "last_block.gasLimit": block.gasLimit,
        "web3.eth.generate_gas_price": settings.web3.eth.generate_gas_price(),
        "web3.eth.gasPrice": settings.web3.eth.gasPrice
    })
    return result
