"""
Check permissions. 

12223334455 is a custom testing number used in the permissions
database. It has permissions to use _all_ apps. 

00000000000 is a custom testing number
in the permissions database. It has permissions to use _only_ the groceries app.
"""
import permissions

# Fixtures
from . import user_git_pytest, users_dup_namephone


def test_check_permissions(user_git_pytest):
    assert permissions.check_permissions(
        "12223334455", "wordhunt"
    )


def test_custom_permissions(users_dup_namephone):
    assert permissions.check_permissions(
        "10101010101", "groceries"
    )


def test_no_permissions_no_user():
    assert not permissions.check_permissions(
        "09876543212", "groceries"
    )


def test_no_permissions_user_exists(users_dup_namephone):
    """
    The Dup Namephone user should only have access to groceries and apps,
    in separate logs.
    """
    assert not permissions.check_permissions(
        "10101010101", "cocktails"
    )


def test_db_init():
    key = permissions.db_init()
    permissions.permissions_db.delete(key)
