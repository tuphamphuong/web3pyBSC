import logging
import sys

import uvicorn
import time
from fastapi import FastAPI, Depends, Request
from pydantic.tools import lru_cache
from app.config.service_setting import Settings
from app.api import transaction_api, account_api, contract_api, internal_api, gas_api, receipt_api
from loguru import logger
from starlette.routing import Match

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")

app = FastAPI()
app.include_router(internal_api.router)
app.include_router(gas_api.router)
app.include_router(account_api.router)
app.include_router(transaction_api.router)
app.include_router(receipt_api.router)
app.include_router(contract_api.router)


@lru_cache()
def get_settings():
    return Settings()


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response


@app.get("/")
def get(settings: Settings = Depends(get_settings)):
    return {"app": settings.app_name}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8888)
