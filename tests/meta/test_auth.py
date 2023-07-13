"""
Test new user authentication, from getting their user code to redirecting them
to Zapier to get their access tokens.
"""
# External
import pytest
from fastapi.testclient import TestClient

# App
from api import app
from jeeves.keys import KEYS


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app=app)


def test_user_by_phone(test_client):
    """Test getting a user by their phone number."""
    res = test_client.get(
        f"/auth/user-by-phone/{KEYS.Twilio.my_number}",
        params={"access_code": KEYS.General.auth_access_code},
    )

    assert res.status_code == 200
    assert "user" in res.json()


def test_invalid_access_code(test_client):
    """Test getting a user by their phone number with an invalid access code."""
    res = test_client.get(
        f"/auth/user-by-phone/{KEYS.Twilio.my_number}",
        params={"access_code": "invalid"},
    )

    assert res.status_code == 200
    assert "error" in res.json()


def test_zapier_redirect_link(test_client):
    """Test getting the link to redirect a user to Zapier."""
    # Get the user code
    user_code = test_client.get(
        f"/auth/user-by-phone/{KEYS.Twilio.my_number}",
        params={"access_code": KEYS.General.auth_access_code},
    ).json()["user"]

    # Get the redirect link
    res = test_client.get(f"/auth/zapier-start/{user_code}")
    assert res  # there's really no logic to be tested as it's all string formatting.
