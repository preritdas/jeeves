"""Utilities for everything."""
import requests

from functools import wraps

from jeeves.keys import KEYS


def app_handler(app_help: str, app_options: dict = {}):
    """
    Handler decorator that automatically returns help options if requested in
    the handler's required `options` parameter.
    """
    app_help += "\n\n"

    def wrapper_func(function):
        @wraps(function)
        def inner(content: str, options: dict[str, str]) -> str:
            if not "help" in options:
                return function(content, options)

            if not app_options:
                return app_help + "There are no available options."

            option_messages = []
            for option, message in app_options.items():
                option_messages.append(f"- {option.lower()}: {message.lower()}")

            return app_help + "Available options:\n" + "\n".join(option_messages)

        return inner

    return wrapper_func


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


# ---- Web stuff ----

REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) " "Gecko/20100101 Firefox/12.0"
    ),
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html",
    "Referer": "https://www.google.com",
}


# ---- Zapier ----

def access_token_expired(access_token: str) -> bool:
    """Determine if an access token has expired."""
    url = "https://nla.zapier.com/api/v1/check"
    res = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return not res.json()["success"]


def refresh_zapier_access_token(refresh_token: str) -> str:
    """Generate a new access token if the old one is expired."""
    url = "https://nla.zapier.com/oauth/token/"
    res = requests.post(
        url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "client_id": KEYS.Zapier.client_id,
            "client_secret": KEYS.Zapier.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    )

    res.raise_for_status()
    return res.json()["access_token"]
