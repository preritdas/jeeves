from fastapi.testclient import TestClient
import pytest

import api


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app=api.app)


def test_testing_endpoint(test_client):
    res = test_client.get("/")
    assert res.status_code == 200


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
