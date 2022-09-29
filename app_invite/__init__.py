"""Invite a new user to use Jeeves."""
import utils

import texts


APP_HELP = "Invite someone to use Jeeves' services."
APP_OPTIONS = {
    "recipient": "REQUIRED, phone number of the invitee"
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    """Invite new user."""
    if not "recipient" in options:
        return "You must provide a recipient's phone number as an option."
    
    try:
        int(recipient := options["recipient"])
    except ValueError:
        return "Invalid phone number."
    
    invite_content = "Good day, sir. My man has invited you to avail of my services. " \
        "Text me 'app: apps' to see what I can do.\n\n" \
        "To view an app's help, send 'options: help = yes' below your " \
        "app name statement.\n\n" \
        "app: jokes\noptions: help = yes"

    texts.send_message(invite_content, recipient)

    return f"Successfully invited {recipient}. The message sent is below. " \
        f"\n\n{invite_content}"
