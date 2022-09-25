"""
Sending text messages back.
"""
# External
import nexmo

# Project
import keys


sms = nexmo.Sms(
    key = keys.Nexmo.api_key,
    secret = keys.Nexmo.api_secret
)


def send_message(content: str, recipient: str):
    """Send a text message."""
    assert isinstance(recipient, str)

    sms.send_message(
        {
            "from": keys.Nexmo.sender,
            "to": recipient,
            "text": str(content)
        }
    )
