"""Utilities for everything."""
import requests

from functools import wraps
from json import JSONDecodeError

from jeeves.errors import ZapierAuthenticationError
from keys import KEYS


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
    res = requests.get(
        url="https://nla.zapier.com/api/v1/check",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    try:
        res_json = res.json()
    except JSONDecodeError as e:
        raise ZapierAuthenticationError(
            "Failed to check if access token is expired. Response code "
            f"{res.status_code}, content: {res.content}. JSON decode error: {e}"
        )

    if "error" in res_json and "expired_token" in res_json["error"]:
        return True

    if "success" in res_json and res_json["success"]:  # res_json["success"] is True
        return False

    raise ZapierAuthenticationError(
        "Failed to check if access token is expired. Response code "
        f"{res.status_code}, content: {res.content}. Unknown case - error not found "
        "in response, nor success."
    )


def refresh_zapier_access_token(refresh_token: str) -> tuple[str, str]:
    """
    Generate a new access token if the old one is expired.
    
    Returns a tuple of (access_token, refresh_token).
    """
    res = requests.post(
        url="https://nla.zapier.com/oauth/token/",
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
    res_json = res.json()
    return res_json["access_token"], res_json["refresh_token"]
