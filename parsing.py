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

    return True


def is_concat(inbound: dict) -> bool:
    """Determines if an inbound sms is part of a concatenated series of messages."""
    assert isinstance(inbound, dict)
    return "concat" in inbound


def requested_app(inbound: dict) -> tuple[Callable | None, str]:
    """Returns the handler function of an app and its name, or None
    if the app doesn't exist."""
    content: str = inbound["text"]
    first_line = (all_lines := content.splitlines())[0].lower()

    if not "app:" in first_line:
        raise errors.InvalidInbound("No app specified.")

    app_ref_loc = first_line.find("app:") + len("app:")
    app_name = first_line[app_ref_loc:].strip().lower()

    if not app_name in apps.PROGRAMS:
        return None
    
    return apps.PROGRAMS.get(app_name, None), app_name


def check_permissions(user: str, app: str) -> bool:
    """Checks if a user has access to an app.
    
    Implement this later. For now, everyone has access."""
    return True


def _parse_options(options: str) -> dict[str, str]:
    """Takes an options string and returns a dict."""
    options = options.lower()
    assert "options:" in options

    options = options[len("options:"):].strip()
    list_of_options = [ele.strip() for ele in options.split(";")]
    
    return_options = {}
    for option in list_of_options:
        key, val = (ele.strip() for ele in option.split("="))
        return_options[key] = val
    
    return return_options


def app_content_options(inbound: dict) -> tuple[str, dict]:
    """Returns app input content."""
    raw_content: str = inbound["text"]
    lines = raw_content.splitlines()

    content = True
    options = {}
    for pos, line in enumerate(lines):
        line = line.lower()
        if "app:" in line or line == "": 
            continue
        if "options:" in line:
            options = _parse_options(line)
            continue

        break
    else: 
        content = False # if no other lines found

    return "\n".join(lines[pos:]) if content else "", options
