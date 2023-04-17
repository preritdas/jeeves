"""
Parsing inbound messages for content.
"""
from typing import Callable

import pydantic

# Project
import errors
import apps


class InboundMessage(pydantic.BaseModel):
    """
    Inbound structure to be used .
    """
    phone_number: str
    body: str

    @pydantic.validator("phone_number")
    def remove_plus(cls, v):
        """Remove the plus from the phone number."""
        if v[0] == "+":
            return v[1:]
        return v


def assert_valid(inbound: InboundMessage) -> bool:
    """Check that an inbound sms conforms to necessary structure."""
    content: str = inbound.body
    first_line = (all_lines := content.splitlines())[0].lower()

    if not "app:" in first_line:
        return False

    return True


def requested_app(inbound: InboundMessage) -> tuple[Callable | None, str]:
    """Returns the handler function of an app and its name, or None
    if the app doesn't exist."""
    content: str = inbound.body
    first_line = (all_lines := content.splitlines())[0].lower()

    if not "app:" in first_line:
        raise errors.InvalidInbound("No app specified.")

    app_ref_loc = first_line.find("app:") + len("app:")
    app_name = first_line[app_ref_loc:].strip().lower()

    if not app_name in apps.PROGRAMS:
        return None, app_name
    
    return apps.PROGRAMS.get(app_name), app_name


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


def app_content_options(inbound: InboundMessage) -> tuple[str, dict]:
    """Returns app input content."""
    raw_content: str = inbound.body
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
