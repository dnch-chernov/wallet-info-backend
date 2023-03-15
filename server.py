"""
Simple API server that returns balance for ETH and USDC wallets.
"""
import json
import os

from fastapi import Depends, FastAPI, HTTPException
from web3 import Web3

from error_messages import ErrorMessage

provider = os.getenv("PROVIDER_URL", "http://localhost:8545")
usdc_contract_address = os.getenv("USDC_CONTRACT_ADDRESS")
app = FastAPI()
w3 = Web3(Web3.HTTPProvider(provider))
with open("abi.json", "r", encoding="UTF-8") as abi_file:
    abi = json.load(abi_file)
contract = w3.eth.contract(
    address=Web3.toChecksumAddress(usdc_contract_address), abi=abi
)


def get_eth_balance(address: str):  # pragma: no cover
    """
    Return ETH balance from ETH node
    """
    return w3.eth.get_balance(Web3.toChecksumAddress(address))


def get_usdc_balance(address: str):  # pragma: no cover
    """
    Return USDC balance from ETH node
    """
    return contract.functions.balanceOf(Web3.toChecksumAddress(address)).call()


def get_w3_connected():  # pragma: no cover
    """
    Return Web3 connection status
    """
    return w3.isConnected()


@app.get("/balance/{crypto}/{address}")
def get_balance(
    crypto: str,
    address: str,
    is_connected: bool = Depends(get_w3_connected),
    eth_balance: str = Depends(get_eth_balance),
    usdc_balance: str = Depends(get_usdc_balance),
):
    """
    GET /balance/crypto/address
    """
    if not is_connected:
        raise HTTPException(status_code=503, detail=ErrorMessage.NODE_UNAVAILABLE.value)
    try:
        Web3.toChecksumAddress(address)
    except ValueError as error:
        raise HTTPException(
            status_code=400, detail=ErrorMessage.INVALID_ADDRESS.value
        ) from error
    if crypto == "eth":
        wei = eth_balance
        balance = Web3.fromWei(wei, "ether")
    elif crypto == "usdc":
        wei = usdc_balance
        balance = Web3.fromWei(wei, "mwei")
    else:
        raise HTTPException(status_code=400, detail=ErrorMessage.INVALID_CRYPTO.value)
    return {"crypto": crypto, "balance": balance}


@app.get("/status")
def status(is_connected: bool = Depends(get_w3_connected)):
    """
    web3 connection status
    """
    return {"connected": is_connected}
