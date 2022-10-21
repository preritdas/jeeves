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

    cases = [
        "No users were found",
        "Nobody with name",
        "Nobody was found"
    ]

    assert any(case in res for case in cases)


def test_no_action():
    res = app_permissions.handler(
        content = "",
        options = {}
    )

    assert "You must provide an action" in res


def test_no_content():
    res = app_permissions.handler(
        content = "",
        options = {"action": "update"}
    )

    assert "You must provide" in res


def test_duplicate_phones():
    """
    11111111111 is a double entry in the permissions database, purely
    for the sake of this test.
    """
    res = app_permissions.handler(
        content = "something",
        options = {"action": "view", "phone": "11111111111"}
    )

    assert "exists multiple times" in res
    assert "mistake" in res  # duplicate phones should never happen


def test_no_name_found():
    res = app_permissions.handler(
        content = "something",
        options = {"action": "view", "name": "i dont exist"}
    )

    assert "wasn't found" in res


def test_view_permissions():
    """
    Note on the duplicates test: Duplicate Name is a name used twice in the 
    permissions database to facilitate this test.
    """
    res = app_permissions.handler(
        "",
        {"inbound_phone": "12223334455", "action": "view", "name": "git pytest"}
    )
    assert "all" in res

    # Test with phone query
    res = app_permissions.handler(
        "",
        {"inbound_phone": "12223334455", "action": "view", "phone": "12223334455"}
    )
    assert "all" in res

    # Test no result query
    res = app_permissions.handler(
        "",
        {"inbound_phone": "12223334455", "action": "view", "phone": "11011011100"}
    )
    assert "doesn't exist" in res

    # Test too many
    res = app_permissions.handler(
        "",
        {"inbound_phone": "12223334455", "action": "view", "name": "duplicate name"}
    )
    assert "multiple people were found" in res.lower()


def test_help():
    res = app_permissions.handler(
        content = "",
        options = {"help": "yes"}
    )

    assert "'create'" in res
