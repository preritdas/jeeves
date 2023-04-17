"""Fixtures etc."""
import pytest

import datetime as dt
import string
import random

import usage  # fixture for temporary logs for report
import permissions  # fixtures for temporary users


@pytest.fixture(scope="session")
def default_inbound() -> dict[str, str]:
    random_inbound = "".join(
        [str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) for _ in range(10)]
    )

    return {
        "phone_number": random_inbound,
        "body": "app: apps",
    }


@pytest.fixture
def default_options(default_inbound) -> dict[str, str]:
    return {"inbound_phone": default_inbound["phone_number"]}


@pytest.fixture(scope="session")
def user_only_groceries() -> dict[str, str]:
    """
    Temporary user who only has access to the groceries app.

    Test calling another app with only these permissions to test
    permissions edge case.
    """
    first_name = "".join(random.sample(string.ascii_lowercase, 5)).title()
    last_name = "".join(random.sample(string.ascii_lowercase, 5)).title()

    phone = "".join(
        [str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) for _ in range(10)]
    )

    user_attrs = {
        "Name": f"{first_name} {last_name}",
        "Permissions": "groceries",
        "Phone": phone
    }

    key = permissions.permissions_db.put(user_attrs)["key"]
    yield user_attrs
    permissions.permissions_db.delete(key)


@pytest.fixture(scope="session")
def user_git_pytest(default_inbound) -> dict[str, str]:
    """Temporary random user with maximum permissions."""
    first_name = "".join(random.sample(string.ascii_lowercase, 5)).title()
    last_name = "".join(random.sample(string.ascii_lowercase, 5)).title()

    user_attrs = {
        "Name": f"{first_name} {last_name}",
        "Permissions": "all",
        "Phone": default_inbound["phone_number"]
    }

    key = permissions.permissions_db.put(user_attrs)["key"]
    yield user_attrs
    permissions.permissions_db.delete(key)


@pytest.fixture(scope="session")
def users_dup_namephone() -> list[dict[str, str]]:
    """
    Temporary users with the same name and phone number to test
    handling duplicate entries.
    """
    first_name = "".join(random.sample(string.ascii_lowercase, 5)).title()
    last_name = "".join(random.sample(string.ascii_lowercase, 5)).title()

    phone_number = "".join(
        [str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) for _ in range(10)]
    )

    users = [
        {
            "Name": " ".join([first_name, last_name]),
            "Permissions": "groceries",
            "Phone": phone_number
        },
        {
            "Name": " ".join([first_name, last_name]),
            "Permissions": "apps",
            "Phone": phone_number
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
