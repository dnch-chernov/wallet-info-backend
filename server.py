"""
Simple API server that returns balance for ETH and USDC wallets.
"""
import json
import os

from fastapi import FastAPI, HTTPException
from web3 import Web3

from error_messages import ErrorMessage

provider = os.getenv("PROVIDER_URL")
usdc_contract_address = os.getenv("USDC_CONTRACT_ADDRESS")
app = FastAPI()
w3 = Web3(Web3.HTTPProvider(provider))
with open("abi.json", "r", encoding="UTF-8") as abi_file:
    abi = json.load(abi_file)
contract = w3.eth.contract(
    address=Web3.toChecksumAddress(usdc_contract_address), abi=abi
)


@app.get("/balance/{crypto}/{address}")
async def eth_balance(crypto: str, address: str):
    """
    GET /balance/crypto/address
    """
    if not w3.isConnected():
        raise HTTPException(status_code=503, detail=ErrorMessage.NODE_UNAVAILABLE.value)
    if crypto not in ["eth", "usdc"]:
        raise HTTPException(status_code=400, detail=ErrorMessage.INVALID_CRYPTO.value)
    try:
        valid_address = Web3.toChecksumAddress(address)
    except ValueError as error:
        raise HTTPException(
            status_code=400, detail=ErrorMessage.INVALID_ADDRESS.value
        ) from error
    if crypto == "eth":
        wei = w3.eth.get_balance(valid_address)
        balance = w3.fromWei(wei, "ether")
    elif crypto == "usdc":
        wei = contract.functions.balanceOf(Web3.toChecksumAddress(valid_address)).call()
        balance = w3.fromWei(wei, "mwei")
    return {"crypto": crypto, "balance": balance}

@app.get("/status")
async def status():
    """
    Status endpoint.
    """
    return {"status": "Still alive!"}
