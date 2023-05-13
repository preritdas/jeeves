"""
Check permissions. 

Using session scoped fixtures, defined in tests/__init__.py, for the users formerly
Git Pytest and Dup Namephone. Their names and phone numbers are now randomized so tests
can be run concurrently without causing errors with duplicate values in the database
causing un-tested-for results.
"""
from jeeves import permissions


def test_check_permissions(user_git_pytest):
    assert permissions.check_permissions(user_git_pytest["Phone"], "wordhunt")


def test_custom_permissions(users_dup_namephone):
    assert permissions.check_permissions(users_dup_namephone[0]["Phone"], "groceries")


def test_no_permissions_no_user():
    assert not permissions.check_permissions("09876543212", "groceries")


def test_no_permissions_user_exists(users_dup_namephone):
    """
    The Dup Namephone user should only have access to groceries and apps,
    in separate logs.
    """
    assert not permissions.check_permissions("10101010101", "cocktails")


def test_wrong_app_permissions(user_only_groceries):
    """
    Test the edge case in which a user has access to a limitied, specific set
    of apps but tries to use another app which he doesn't have access to.
    """
    assert not permissions.check_permissions(user_only_groceries["Phone"], "cocktails")


def test_db_init():
    key = permissions.db_init()
    permissions.permissions_db.delete(key)


def test_auto_db_init(mocker):
    """The line is still not being run, 36 of permissions.py."""
    mocker.patch("jeeves.permissions.deta.base.FetchResponse.items", [])

    assert not permissions.permissions_db.fetch().items
