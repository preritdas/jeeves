import permissions


def test_check_permissions():
    assert permissions.check_permissions(
        "12223334455", "wordhunt"
    )
