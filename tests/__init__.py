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
def temp_usage_logs():
    """
    Generate two temporary elements in the usage log so a usage report
    can be generated on that log. Delete the log afterwards.
    """
    usage_payloads = [
        {
            "phone_number": "12223334455",
            "app_name": "groceries",
            "content": "apples\nbananas",
            "options": {"setup": "whole foods"},
            "time": dt.datetime.now()
        },
        {
            "phone_number": "12223334455",
            "app_name": "cocktails",
            "content": "vesper",
            "options": {"inbound_phone": "12223334455"},
            "time": dt.datetime.now()
        }
    ]

    keys = [usage.log_use(**payload) for payload in usage_payloads]
    yield usage_payloads

    # Remove the temporary logs
    for key in keys:
        usage.usage_db.delete(key)
