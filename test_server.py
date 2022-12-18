"""
Unit tests for API server.
"""
from fastapi.testclient import TestClient

from error_messages import ErrorMessage
from server import app

VALID_ADDRESS = "0x300045c41b5334772C25196ac0035bCDD511a821"
ETH_VALUE = 0.024925767330357064
USDC_VALUE = 61.280028
client = TestClient(app)


class TestServer:
    """
    Test api endpoints.
    """

    def test_happy_path_eth(self):
        """
        Get ETH balance
        """
        response = client.get(f"/balance/eth/{VALID_ADDRESS}")
        assert response.status_code == 200
        assert response.json() == {"crypto": "eth", "balance": ETH_VALUE}

    def test_happy_path_usdc(self):
        """
        Get USDC balance
        """
        response = client.get(f"/balance/usdc/{VALID_ADDRESS}")
        assert response.status_code == 200
        assert response.json() == {"crypto": "usdc", "balance": USDC_VALUE}

    def test_invalid_crypto(self):
        """
        Check invalid crypto name
        """
        response = client.get(f"/balance/usdt/{VALID_ADDRESS}")
        assert response.status_code == 400
        assert response.json() == {"detail": ErrorMessage.INVALID_CRYPTO.value}

    def test_invalid_address(self):
        """
        Check invalid wallet address
        """
        response = client.get("/balance/eth/abc")
        assert response.status_code == 400
        assert response.json() == {"detail": ErrorMessage.INVALID_ADDRESS.value}

    def test_status(self):
        """
        Check status endpoint
        """
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"status": "Still alive!"}
