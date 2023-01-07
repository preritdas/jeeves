from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app=app)


def test_testing_endpoint(test_client):
    res = test_client.get("/")

    assert "All working here" in res.text
    assert res.status_code == 200
