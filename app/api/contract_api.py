from fastapi import APIRouter, Depends
from loguru import logger
from pydantic.tools import lru_cache
from solcx import compile_source

from app.config.service_setting import Settings
from app.contract.erc721_contract import sol

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
)


@lru_cache()
def get_settings():
    return Settings()

# Deploy contract
@router.post("/erc721/")
def post(item_id: str, settings: Settings = Depends(get_settings)):
    #TODO: Set item_id in sol source
    web3 = settings.web3

    # Create account from private key
    acc = web3.eth.account.from_key(settings.account_from_private_key)
    acc_checksum = web3.toChecksumAddress(acc.address)

    # Set default acc to use in transact
    web3.eth.default_account = acc_checksum
    logger.debug(f"web3.eth.getBalance {web3.eth.getBalance(acc.address)}")

    compiled_sol = compile_source(sol)

    # Retrieve the contract interface
    contract_id, contract_interface = compiled_sol.popitem()
    logger.debug(f"contract_id {contract_id} contract_interface {contract_interface}")

    # get bytecode / bin
    bytecode = contract_interface['bin']
    logger.debug(f"bytecode {bytecode}")

    # get abi
    abi = contract_interface['abi']
    logger.debug(f"abi {abi}")

    Contract = web3.eth.contract(abi=abi , bytecode=bytecode)

    tx = Contract.constructor().buildTransaction({
        'chainId': settings.bsc_net_chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei(20, 'gwei'),
        'nonce': web3.eth.getTransactionCount(acc.address, 'pending'),
    })
    signed = web3.eth.account.signTransaction(tx, settings.account_from_private_key)
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
    print(f"Contract deployed; {tx_hash.hex()} Waiting to transaction receipt")

    web3.eth.waitForTransactionReceipt(tx_hash, timeout=600, poll_latency=10)
    logger.debug("Wait done")

    # Get transaction receipt
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    logger.debug(f"w3.eth.get_transaction_receipt {receipt}")

    result = dict({
        "blockHash": receipt["blockHash"].hex(),
        "blockNumber": receipt["blockNumber"],
        "contractAddress": receipt["contractAddress"],
        "cumulativeGasUsed": receipt["cumulativeGasUsed"],
        "from": receipt["from"],
        "gasUsed": receipt["gasUsed"],
        "logs": receipt["logs"],
        "logsBloom": receipt["logsBloom"].hex(),
        "status": receipt["status"],
        "to": receipt["to"],
        "transactionHash": receipt["transactionHash"].hex(),
        "transactionIndex": receipt["transactionIndex"],
        "type": receipt["type"],
    })
    return result
