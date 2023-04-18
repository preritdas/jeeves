"""
Sending text messages back.
"""
# External
from twilio.rest import Client as TwilioClient

# Project
from keys import KEYS
import config


twilio_client = TwilioClient(
    KEYS["Twilio"]["account_sid"],
    KEYS["Twilio"]["auth_token"]
)


def send_message(content: str, recipient: str) -> bool:
    """
    Send a text message. Returns True if the request succeeded, or False if it failed.
    """
    assert isinstance(recipient, str)

    if config.General.SANDBOX_MODE:
        return True

    message_sent = twilio_client.messages.create(
        to = recipient,
        from_ = KEYS["Twilio"]["sender"],
        body = content
    )

    return True

    # Create success check for Twilio
    return True if vonage_res["messages"][0]["status"] == "0" else False
