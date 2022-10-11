"""
Check permissions. 

12223334455 is a custom testing number used in the permissions
database. It has permissions to use _all_ apps. 

00000000000 is a custom testing number
in the permissions database. It has permissions to use _only_ the groceries app.
"""
import permissions


def test_check_permissions():
    assert permissions.check_permissions(
        "12223334455", "wordhunt"
    )


def test_custom_permissions():
    assert not permissions.check_permissions(
        "00000000000", "wordhunt"
    )

    assert permissions.check_permissions(
        "00000000000", "groceries"
    )
