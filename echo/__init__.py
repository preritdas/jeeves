from re import L
import texts


def handler(content: str, options: dict) -> str:
    """Send texts."""
    if options.get("help", None):
        return "Send a message (content) to someone else on my behalf. \n\n" \
            "Available options:\n" \
            "- recipient: recipient's phone number"

    if not "recipient" in options:
        return "You must provide the recipient's phone number as an option."
    
    texts.send_message(content, options["recipient"])

    return f"The following message was sent to {options['recipient']}:\n\n{content}"
