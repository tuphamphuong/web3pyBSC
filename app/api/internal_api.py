from fastapi import APIRouter, Depends, HTTPException
from pydantic.tools import lru_cache

from app.config.service_setting import Settings

router = APIRouter(
    prefix="/internals",
    tags=["internals"],
)

@lru_cache()
def get_settings():
    return Settings()


@router.get("/configs")
def get(settings: Settings = Depends(get_settings)):

    result = dict({
        "app_name": settings.app_name,
        "bsc_net_url": settings.bsc_net_url,
        "bsc_net_chain_id": settings.bsc_net_chain_id,
        "account_from": settings.account_from,
        "account_to": settings.account_to,
    })
    return result


@router.get("/connections")
def get(settings: Settings = Depends(get_settings)):

    result = dict({
        "clientVersion": settings.web3.clientVersion,
        "isConnected": settings.web3.isConnected(),
        "eth.block_number": settings.web3.eth.block_number,
        "net.peer_count": settings.web3.net.peer_count,
    })
    return result

