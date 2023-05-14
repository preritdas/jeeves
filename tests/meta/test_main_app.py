"""
Test the main app, including the main handler and the main app itself.
Testing API handlers, routers, endpoints, etc. using a FastAPI TestClient.
"""
from fastapi.testclient import TestClient
import pytest

import api
from api.telegram_inbound import process_telegram_inbound
from jeeves.keys import KEYS


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app=api.app)


def test_testing_endpoint(test_client):
    res = test_client.get("/")
    assert res.status_code == 200


# ---- Texts ----

def test_apps_non_threaded(test_client, default_inbound, mocker):
    mocker.patch("api.text_inbound.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.inbound.usage.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.CONFIG.General.threaded_inbound", False)

    res = test_client.post(
        "/texts/inbound-sms",
        data={"From": default_inbound["phone_number"], "Body": default_inbound["body"]},
    )
    assert res.status_code == 204


def test_apps_threaded(test_client, default_inbound, mocker):
    mocker.patch("api.text_inbound.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.inbound.usage.CONFIG.General.sandbox_mode", True)
    mocker.patch("api.text_inbound.CONFIG.General.threaded_inbound", True)

    res = test_client.post(
        "/texts/inbound-sms",
        data={"From": default_inbound["phone_number"], "Body": default_inbound["body"]},
    )
    assert res.status_code == 204


# ---- Telegram ----

def test_telegram_text(mocker):
    mocker.patch("api.telegram_inbound.CONFIG.General.sandbox_mode", True)

    response = process_telegram_inbound(1101010101, "Hi.")

    assert response
    assert isinstance(response, str)
    assert "don't recognize" in response


def test_telegram_endpoint(mocker, test_client):
    mocker.patch("api.telegram_inbound.CONFIG.General.sandbox_mode", True)
    text_payload = {
        "message": {
            "from": {"id": 000000000},
            "text": "Hi."
        }
    }

    res = test_client.post("/telegram/inbound-telegram", json=text_payload)
    assert res.status_code == 200
