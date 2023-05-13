"""
Sending text messages back.
"""
# External
from twilio.rest import Client as TwilioClient

# Standard
import time

# Project
from jeeves.keys import KEYS
from jeeves.config import CONFIG


twilio_client = TwilioClient(KEYS.Twilio.account_sid, KEYS.Twilio.auth_token)


def extract_base_url(url: str) -> str:
    """Takes an HTTP URL path and extracts the base url."""
    # Find the index of the first "/" after the "https://" part of the URL
    end_index = url.find("/", len("https://"))
    # Return the substring from the beginning of the URL to the first "/"
    return url[:end_index]


# Get the deployed base url. Currently not needed as using UploadIO.
BASE_URL = extract_base_url(
    twilio_client.incoming_phone_numbers.get(KEYS.Twilio.sender_sid).fetch().voice_url
)

TWILIO_NON_SUCCESS_STATUS: set[str] = {
    "queued",
    "failed",
    "undelivered",
    "receiving",
    "accepted",
    "scheduled",
    "partially_delivered",
    "canceled"
}


def send_message(content: str, recipient: str) -> bool:
    """
    Send a text message. Returns True if the request succeeded, or False if it failed.
    """
    assert isinstance(recipient, str)

    if CONFIG.General.sandbox_mode:
        return True

    message_sent = twilio_client.messages.create(
        to=recipient, from_=KEYS.Twilio.sender, body=content
    )

    # Try twice for one second total for success
    for _ in range(2):
        if (
            last_status := message_sent.fetch().status
        ) not in TWILIO_NON_SUCCESS_STATUS:
            return True

        time.sleep(0.5)

    return False
