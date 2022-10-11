import app_permissions


def test_handler():
    res = app_permissions.handler(
        content = "all",
        options = {
            "action": "create",
            "phone": "12223334455",
            "name": "git pytest"
        }
    )

    assert "Added permissions" in res or "Git Pytest already exists" in res

    # Test querying with a wrong name
    res = app_permissions.handler(
        content = "all",
        options = {
            "action": "create",
            "phone": "12223334455",
            "name": "bad name"
        }
    )

    assert "12223334455 already exists" in res

    # Test updating
    res = app_permissions.handler(
        content = "all",
        options = {
            "action": "update",
            "phone": "12223334455"
        }
    )

    assert "Successfully changed" in res

    # Test updating query by name
    res = app_permissions.handler(
        content = "all",
        options = {
            "action": "update",
            "name": "git pytest"
        }
    )

    assert "successfully" in res.lower()

    # Test updating with none found
    res = app_permissions.handler(
        content = "all",
        options = {
            "action": "update",
            "name": "87asdcgaysdc"
        }
    )

    assert "No users were found" in res or "Nobody with name" in res


def test_help():
    res = app_permissions.handler(
        content = "",
        options = {"help": "yes"}
    )

    assert "'create'" in res
