"""Very inbounds from various sources."""
from fastapi import Request
from twilio.request_validator import RequestValidator

from jeeves.texts import BASE_URL
from jeeves.keys import KEYS


# Create Twilio request validator
twilio_validator = RequestValidator(KEYS.Twilio.auth_token)


async def validate_twilio_request(request: Request) -> bool:
    """Use the auth token and request url and form to verify."""
    if "X-Twilio-Signature" not in request.headers:
        return False

    # Get the request url
    url = BASE_URL + request.url.path

    # Get the request form
    form = await request.form()

    # Validate the request
    return twilio_validator.validate(url, form, request.headers["X-Twilio-Signature"])


async def validate_telegram_request(request: Request) -> bool:
    """Use the auth token and request url and form to verify."""
    if "X-Telegram-Bot-Api-Secret-Token" not in request.headers:
        return False

    # Validate the request
    return request.headers["X-Telegram-Bot-Api-Secret-Token"] == \
        KEYS.Telegram.api_secret_token
