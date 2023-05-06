"""
Parsing inbound messages for content.
"""
from typing import Callable

import pydantic

# Project
import apps


def _parse_options(options: str) -> dict[str, str]:
    """Takes an options string and returns a dict."""
    options = options.lower()
    assert "options:" in options

    options = options[len("options:") :].strip()
    list_of_options = [ele.strip() for ele in options.split(";")]

    return_options = {}
    for option in list_of_options:
        key, val = (ele.strip() for ele in option.split("="))
        return_options[key] = val

    return return_options


def validate_phone_number(phone_number: str) -> str:
    """Standardize and validate input phone number. Raise ValueError if invalid."""
    try:
        phone_number = str(phone_number)
    except ValueError:
        raise ValueError(f"Couldn't interpret {phone_number} as a string.")
        
    if not phone_number:
        raise ValueError("Phone number was given as an empty string.")

    # Remove the plus if given, ex. Twilio does
    if phone_number[0] == "+":
        phone_number = phone_number[1:]

    if not phone_number.isnumeric():
        raise ValueError(f"Resulting phone number {phone_number} is not numeric.")

    if len(phone_number) != 11:
        raise ValueError(
            f"Phone number {phone_number} isn't 11 digits. Does it have a country code?"
        )
        
    # Otherwise, if all looks good
    return phone_number


class InboundMessage(pydantic.BaseModel):
    """
    Inbound structure to be used .
    """
    phone_number: str
    body: str

    @pydantic.validator("phone_number")
    def remove_plus(cls, v):
        """Remove the plus from the phone number."""
        return validate_phone_number(v)

    @property
    def valid(self) -> bool:
        """Check that an inbound sms conforms to necessary structure."""
        content: str = self.body
        first_line = (all_lines := content.splitlines())[0].lower()

        if not "app:" in first_line:
            return False

        return True

    @property
    def requested_app(self) -> tuple[Callable | None, str]:
        """Returns the handler function of an app and its name, or None
        if the app doesn't exist."""
        content: str = self.body
        first_line = (all_lines := content.splitlines())[0].lower()

        if not "app:" in first_line:
            return apps.PROGRAMS["gpt"], "gpt"

        app_ref_loc = first_line.find("app:") + len("app:")
        app_name = first_line[app_ref_loc:].strip().lower()

        if not app_name in apps.PROGRAMS:
            return None, app_name

        return apps.PROGRAMS.get(app_name), app_name

    @property
    def app_content_options(self) -> tuple[str, dict]:
        """Returns app input content."""
        # If using default GPT
        if not self.valid:  # ergo, using GPT
            return self.body, {}

        raw_content: str = self.body
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
            content = False  # if no other lines found

        return "\n".join(lines[pos:]) if content else "", options
