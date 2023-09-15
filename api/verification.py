"""Very inbounds from various sources."""
from fastapi import Request
from twilio.request_validator import RequestValidator

from jeeves.texts import BASE_URL
from keys import KEYS
from config import CONFIG


# Create Twilio request validator
twilio_validator = RequestValidator(KEYS.Twilio.auth_token)


async def validate_twilio_request(request: Request, path: str = "") -> bool:
    """
    Use the auth token and request url and form to verify.
    
    Args:
        request (Request): The request to validate.
        path (str, optional): Optional path. Provide this for outbound calls as 
            the call id at the end is used when Twilio hashes.
    """
    # If validation is off, don't validate
    if not CONFIG.Security.validate_twilio_inbound:
        return True

    if "X-Twilio-Signature" not in request.headers:
        return False

    # Get the request url
    if not path:
        path = request.url.path

    url = BASE_URL + path

    # Get the request form
    form = await request.form()

    # Validate the request
    return twilio_validator.validate(url, form, request.headers["X-Twilio-Signature"])


async def validate_telegram_request(request: Request) -> bool:
    """Use the auth token and request url and form to verify."""
    # If validation is off, don't validate
    if not CONFIG.Security.validate_telegram_inbound:
        return True

    if "X-Telegram-Bot-Api-Secret-Token" not in request.headers:
        return False

    # Validate the request
    return request.headers["X-Telegram-Bot-Api-Secret-Token"] == \
        KEYS.Telegram.api_secret_token
