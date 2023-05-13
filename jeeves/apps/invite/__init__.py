"""Invite a new user to use Jeeves."""
from jeeves import utils
from jeeves import texts


APP_HELP = (
    "Invite someone to use Jeeves' services. Specify the recipient's phone "
    "number in the message content."
)
APP_OPTIONS = {
    "recipient": "REQUIRED, phone number of the invitee",
    "preview": "OPTIONAL, if provided, doesn't text the recipient"
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    """Invite new user."""
    if not content:
        return "You must provide a recipient's phone number as message content."

    try:
        int(recipient := content)
    except ValueError:
        return "Invalid phone number."

    invite_content = (
        "Good day, sir. My man has invited you to avail of my services. "
        "Text me 'app: apps' to see what I can do.\n\n"
        "To view an app's help, send 'options: help = yes' below your "
        "app name statement.\n\n"
        "app: jokes\noptions: help = yes"
    )

    if options.get("preview"):
        return (
            f"Preview of message to be sent to {recipient} below.\n\n{invite_content}"
        )

    if not texts.send_message(invite_content, recipient):
        return "There was an error delivering that text message to the recipient."

    return (
        f"Successfully invited {recipient}. The message sent is below. "
        f"\n\n{invite_content}"
    )
