"""Test the base userless agent."""
from jeeves.agency import generate_base_agent_response


def test_base_agent():
    assert generate_base_agent_response("Hi.")


def test_search():
    assert generate_base_agent_response("weather in washington dc")
  
