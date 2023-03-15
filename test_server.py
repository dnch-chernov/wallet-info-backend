"""
Unit tests for API server.
"""
from fastapi.testclient import TestClient

from web3 import Web3
from error_messages import ErrorMessage
from server import app, get_eth_balance, get_usdc_balance, get_w3_connected

VALID_ADDRESS = "0x300045c41b5334772C25196ac0035bCDD511a821"
ETH_VALUE = 99.99125346475
USDC_VALUE = 61.280028
client = TestClient(app)


def mocked_get_eth_balance():
    """
    Return mocked ETH balance
    """
    return Web3.toWei(ETH_VALUE, "ether")


def mocked_get_usdc_balance():
    """
    Return mocked USDC balance
    """
    return Web3.toWei(USDC_VALUE, "mwei")


def mocked_w3_connected():
    """
    Mock Web3 node status as connected
    """
    return True


def mocked_w3_disconnected():
    """
    Mock Web3 node status as disconnected
    """
    return False


app.dependency_overrides[get_eth_balance] = mocked_get_eth_balance
app.dependency_overrides[get_usdc_balance] = mocked_get_usdc_balance
app.dependency_overrides[get_w3_connected] = mocked_w3_connected


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

    def test_status_connected(self):
        """
        Check status endpoint with connected ETH node
        """
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"connected": True}

    def test_status_disconnected(self):
        """
        Check status endpoint with disconnected ETH node
        """
        app.dependency_overrides[get_w3_connected] = mocked_w3_disconnected
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"connected": False}

    def test_balance_disconnected(self):
        """
        Check balance endpoint with disconnected ETH node
        """
        app.dependency_overrides[get_w3_connected] = mocked_w3_disconnected
        response = client.get(f"/balance/eth/{VALID_ADDRESS}")
        assert response.status_code == 503
        assert response.json() == {"detail": ErrorMessage.NODE_UNAVAILABLE.value}
