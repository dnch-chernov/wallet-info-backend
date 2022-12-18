"""
Enum to store erro messages text.
"""
from enum import Enum


class ErrorMessage(Enum):
    """
    Error messages
    """

    NODE_UNAVAILABLE = "Blockchain node is unavailable"
    INVALID_CRYPTO = "Invalid cryptocurrency"
    INVALID_ADDRESS = "Invalid wallet address"
