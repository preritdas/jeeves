"""Test the base userless agent."""
from jeeves.agency import generate_base_agent_response


def test_base_agent(mocker, callback_uid):
    """Test getting any response from the base agent."""
    mocker.patch("jeeves.agency.uuid.uuid4", return_value=callback_uid)
    assert generate_base_agent_response("Hi.")


def test_search(mocker, callback_uid):
    """Test using a single generic tool."""
    mocker.patch("jeeves.agency.uuid.uuid4", return_value=callback_uid)
    assert generate_base_agent_response("weather in washington dc")
 