"""Test the permissions app."""
import pytest

import random
import string

import app_permissions


def test_handler():
    """Just make sure it's working."""
    assert app_permissions.handler("", {"inbound_phone": "12223334455"})


def test_no_action():
    """Test behavior when no action is specified."""
    res = app_permissions.handler(
        content = "",
        options = {"inbound_phone": "12223334455"}
    )

    assert "You must provide an action" in res


def test_missing_content():
    """Test behavior when content is missing and the action isn't viewing."""
    res = app_permissions.handler(
        content = "",
        options = {
            "inbound_phone": "12223334455",
            "action": "update"
        }
    )

    assert "as content when" in res


# ---- Create ----

def test_creating_deleting(default_options):
    """These are tested together so that the created user can be deleted."""
    random_name = "".join(
        random.sample(
            population = string.ascii_letters,
            k = 8
        )
    )

    res = app_permissions.handler(
        content = "groceries",
        options = {
            "inbound_phone": default_options["inbound_phone"],
            "action": "create",
            "name": random_name,
            "phone": "12344322343"
        }
    )

    assert "Successfully created" in res

    # Delete this user
    res = app_permissions.handler(
        content = "",
        options = {
            "inbound_phone": default_options["inbound_phone"],
            "action": "delete",
            "name": random_name
        }
    )

    assert "Successfully deleted" in res


def test_create_permissions_exist(user_git_pytest):
    res = app_permissions.handler(
        content = "something",
        options = {
            "action": "create",
            "name": user_git_pytest["Name"],
            "phone": user_git_pytest["Phone"]
        }
    )

    assert "already exist" in res


def test_no_data_create():
    res = app_permissions.handler(
        content = "something",
        options = {
            "action": "create"
        }
    )

    assert "both a name and phone number" in res


# ---- View ----

def test_view(user_git_pytest):
    res = app_permissions.handler(
        content = "",
        options = {
            "action": "view",
            "name": user_git_pytest["Name"].lower()
        }
    )

    assert "are below" in res
    assert "all" in res


def test_view_none_found():
    res = app_permissions.handler(
        content = "",
        options = {
            "action": "view",
            "name": "i dont exist"
        }
    )

    assert "I didn't find an" in res


# ---- Update ----

def test_update(user_git_pytest):
    res = app_permissions.handler(
        content = "all",
        options = {
            "action": "update",
            "name": user_git_pytest["Name"].lower()
        }
    )

    assert "Successfully updated" in res
    assert "all" in res


def test_update_none_found():
    res = app_permissions.handler(
        content = "something",
        options = {
            "action": "update",
            "name": "i dont exist"
        }
    )

    assert "I didn't find an" in res


# ---- Delete ----

def test_delete_none_found():
    res = app_permissions.handler(
        content = "something",
        options = {
            "action": "delete",
            "name": "i dont exist"
        }
    )

    assert "I didn't find an" in res


# ---- Errors ----

def test_query_error(users_dup_namephone):
    # By name
    with pytest.raises(app_permissions.query.QueryError):
        app_permissions.query.query(name=users_dup_namephone[0]["Name"])

    # By phone
    with pytest.raises(app_permissions.query.QueryError):
        app_permissions.query.query(phone=users_dup_namephone[0]["Phone"])
