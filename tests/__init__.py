"""Fixtures etc."""
import pytest


@pytest.fixture()
def default_inbound() -> dict[str, str]:
    return {
        "msisdn": "12223334455",
        "text": "app: apps"
    }


@pytest.fixture()
def default_options() -> dict[str, str]:
    return {"inbound_phone": "12223334455"}
