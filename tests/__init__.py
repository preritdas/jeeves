"""Fixtures etc."""
import pytest

import datetime as dt

import usage  # fixture for temporary logs for report


@pytest.fixture()
def default_inbound() -> dict[str, str]:
    return {
        "msisdn": "12223334455",
        "text": "app: apps"
    }


@pytest.fixture()
def default_options() -> dict[str, str]:
    return {"inbound_phone": "12223334455"}


@pytest.fixture(scope="module")
def temp_usage_log():
    """
    Generate a temporary element in the usage log so a usage report
    can be generated on that log. Delete the log afterwards.
    """
    usage_payload = {
        "phone_number": "12223334455",
        "app_name": "groceries",
        "content": "apples\nbananas",
        "options": {"setup": "whole foods"},
        "time": dt.datetime.now()
    }

    key = usage.log_use(**usage_payload)
    yield usage_payload
    usage.usage_db.delete(key)  # remove the temporary log
