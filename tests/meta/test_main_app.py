"""
Test the main app, including the main handler and the main app itself.
Testing API handlers, routers, endpoints, etc. using a FastAPI TestClient.
"""
# External
from fastapi.testclient import TestClient
import pytest

from jeeves.keys import KEYS

import api
from api.telegram_inbound import process_telegram_inbound


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app=api.app)


def test_testing_endpoint(test_client):
    res = test_client.get("/")
    assert res.status_code == 200


# ---- Texts ----

def test_apps_no_auth(test_client, default_inbound, mocker):
    mocker.patch("api.text_inbound.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.inbound.usage.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.CONFIG.General.threaded_inbound", False)

    res = test_client.post(
        "/texts/inbound-sms",
        data={"From": default_inbound["phone_number"], "Body": default_inbound["body"]},
    )
    assert res.status_code == 401


def test_apps_non_threaded(test_client, default_inbound, mocker):
    mocker.patch("api.text_inbound.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.inbound.usage.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.CONFIG.General.threaded_inbound", False)

    # Mock the validator
    mocker.patch("api.verification.RequestValidator.validate", return_value=True)

    data = {
        "From": default_inbound["phone_number"],
        "Body": default_inbound["body"]
    }

    res = test_client.post(
        "/texts/inbound-sms",
        data=data,
        headers={"X-Twilio-Signature": "dummy"}
    )
    assert res.status_code == 204


def test_apps_threaded(test_client, default_inbound, mocker):
    mocker.patch("api.text_inbound.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.inbound.usage.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.CONFIG.General.threaded_inbound", True)

    # Mock the validator
    mocker.patch("api.verification.RequestValidator.validate", return_value=True)

    res = test_client.post(
        "/texts/inbound-sms",
        data={"From": default_inbound["phone_number"], "Body": default_inbound["body"]},
        headers={"X-Twilio-Signature": "dummy"}
    )
    assert res.status_code == 204


# ---- Telegram ----

def test_telegram_text(mocker):
    mocker.patch("api.telegram_inbound.CONFIG.General.sandbox_mode", True)

    response = process_telegram_inbound(1101010101, 1101010011, "Hi.")

    assert response
    assert isinstance(response, str)
    assert "don't recognize" in response


def test_telegram_endpoint(mocker, test_client):
    mocker.patch("api.telegram_inbound.CONFIG.Telegram.threaded_inbound", False)
    mocker.patch("api.telegram_inbound.CONFIG.General.sandbox_mode", True)

    # Create validation header
    headers = {
        "X-Telegram-Bot-Api-Secret-Token": KEYS.Telegram.api_secret_token
    }

    text_payload = {
        "message": {
            "from": {"id": 999999999},
            "text": "Hi.",
            "message_id": 999999999,
        }
    }

    res = test_client.post(
        "/telegram/inbound-telegram", 
        json=text_payload,
        headers=headers
    )

    assert res.status_code == 200
