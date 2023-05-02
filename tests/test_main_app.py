from fastapi.testclient import TestClient
import pytest

import api


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app=api.app)


@pytest.mark.skip
def test_testing_endpoint(test_client):
    res = test_client.get("/")

    assert "All working here" in res.text
    assert res.status_code == 200


@pytest.mark.skip
def test_apps_non_threaded(test_client, default_inbound, mocker):
    mocker.patch("main.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("main.inbound.usage.CONFIG.General.sandbox_mode", True)

    mocker.patch("main.CONFIG.General.threaded_inbound", False)

    json = {**default_inbound}
    del json["concat"]

    res = test_client.post("/inbound-sms", json=json)
    assert res.status_code == 204


@pytest.mark.skip
def test_apps_threaded(test_client, default_inbound, mocker):
    mocker.patch("main.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("main.inbound.usage.CONFIG.General.sandbox_mode", True)

    mocker.patch("main.CONFIG.General.threaded_inbound", True)

    json = {**default_inbound}
    del json["concat"]

    res = test_client.post("/inbound-sms", json=json)
    assert res.status_code == 204
