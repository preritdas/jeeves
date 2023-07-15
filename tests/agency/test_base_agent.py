"""Test the base userless agent."""
import pytest
from fastapi.testclient import TestClient

import api
from jeeves.agency import generate_base_agent_response


@pytest.fixture(scope="module")
def test_client():
    """Create a test client for the API."""
    return TestClient(app=api.app)


# ---- Test via internal generation function ----

def test_base_agent(mocker, callback_uid):
    """Test getting any response from the base agent."""
    mocker.patch("jeeves.agency.uuid.uuid4", return_value=callback_uid)
    assert generate_base_agent_response("Hi.")


def test_search(mocker, callback_uid):
    """Test using a single generic tool."""
    mocker.patch("jeeves.agency.uuid.uuid4", return_value=callback_uid)
    assert generate_base_agent_response("weather in washington dc")
 

# ---- Test via client ----

def test_testing_endpoint(test_client):
    """Test that the testing endpoint is working."""
    res = test_client.get("/")
    assert res.status_code == 200


def test_wrong_password(test_client):
    """Test that the wrong password is rejected."""
    res = test_client.post(
        "/base-agent/run",
        json={"password": "wrong", "query": "hi"},
    )

    assert res.status_code == 401
