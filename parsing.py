"""
Parsing inbound messages for content.
"""
from typing import Callable

# Project
import errors
import apps


def assert_valid(inbound: dict) -> bool:
    """Check that an inbound sms conforms to necessary structure."""
    content: str = inbound["text"]
    first_line = (all_lines := content.splitlines())[0].lower()

    if not "app:" in first_line:
        return False

    # check_lines = all_lines[:]

    # for line in all_lines:
    #     if "options:" in line:
    #         check_lines.remove(line)
    #         break

    # check_lines.pop(0)
    # check_lines = [ele for ele in check_lines if ele]  # remove blank lines

    # if not check_lines
    #     return False

    return True


def is_concat(inbound: dict) -> bool:
    """Determines if an inbound sms is part of a concatenated series of messages."""
    assert isinstance(inbound, dict)
    return "concat" in inbound


def requested_app(inbound: dict) -> Callable | None:
    """Returns the handler function of an app, or None
    if the app doesn't exist."""
    content: str = inbound["text"]
    first_line = (all_lines := content.splitlines())[0].lower()

    if not "app:" in first_line:
        raise errors.InvalidInbound("No app specified.")

    app_ref_loc = first_line.find("app:") + len("app:")
    app_name = first_line[app_ref_loc:].strip().lower()

    if not app_name in apps.PROGRAMS:
        return None
    
    return apps.PROGRAMS.get(app_name, None)


def check_permissions(user: str, app: str) -> bool:
    """Checks if a user has access to an app.
    
    Implement this later. For now, everyone has access."""
    return True


def app_content(inbound: dict) -> str:
    """Returns app input content."""
    raw_content: str = inbound["text"]
    lines = raw_content.splitlines()

    for pos, line in enumerate(lines):
        line = line.lower()
        if "app:" in line or "options:" in line or line == "":
            continue
        break
    
    return "\n".join(lines[pos:])
