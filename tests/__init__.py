"""Fixtures etc."""
import pytest

import datetime as dt

import usage  # fixture for temporary logs for report
import permissions  # fixtures for temporary users


@pytest.fixture
def default_inbound() -> dict[str, str]:
    return {
        "msisdn": "12223334455",
        "text": "app: apps"
    }


@pytest.fixture
def default_options() -> dict[str, str]:
    return {"inbound_phone": "12223334455"}


@pytest.fixture
def user_git_pytest() -> dict[str, str]:
    """Temporary user with maximum permissions."""
    user_attrs = {
        "Name": "Git Pytest",
        "Permissions": "all",
        "Phone": "12223334455"
    }

    key = permissions.permissions_db.put(user_attrs)["key"]
    yield user_attrs
    permissions.permissions_db.delete(key)


@pytest.fixture
def users_dup_namephone() -> list[dict[str, str]]:
    """
    Temporary users with the same name and phone number to test
    handling duplicate entries.
    """
    users = [
        {
            "Name": "Dup Namephone",
            "Permissions": "groceries",
            "Phone": "10101010101"
        },
        {
            "Name": "Dup Namephone",
            "Permissions": "apps",
            "Phone": "10101010101"
        },
    ]

    keys = [permissions.permissions_db.put(payload)["key"] for payload in users]
    yield users

    # Remove the temporary entries
    for key in keys:
        permissions.permissions_db.delete(key)


@pytest.fixture
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
            "app_name": "groceries",
            "content": "chicken",
            "options": {"inbound_phone": "12223334455"},
            "time": dt.datetime.now()
        }
    ]

    keys = [usage.log_use(**payload) for payload in usage_payloads]
    yield usage_payloads

    # Remove the temporary logs
    for key in keys:
        usage.usage_db.delete(key)
