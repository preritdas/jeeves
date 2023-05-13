"""Echo app."""
from jeeves import texts
from jeeves import utils


APP_HELP = "Send a message (content) to someone else on my behalf."
APP_OPTIONS = {"recipient": "recipient's phone number"}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    """Send texts."""
    if not "recipient" in options:
        return "You must provide the recipient's phone number as an option."

    texts.send_message(content, options["recipient"])

    return f"The following message was sent to {options['recipient']}:\n\n{content}"
