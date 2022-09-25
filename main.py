# External
from flask import Flask, request

# Project
import parsing
import texts


app = Flask(__name__)


@app.route("/inbound-sms")
def main_handler():
    """
    Handle all inbound messages.
    
    Keep this as simple as possible, with plenty of outsourcing.
    """
    inbound_sms_content = request.get_json()
    print("\n", inbound_sms_content, sep="")

    if type(inbound_sms_content) is not dict:
        return "", 400

    sender = inbound_sms_content["msisdn"]

    # Valid assertion
    if not parsing.assert_valid(inbound_sms_content):
        texts.send_message(
            "Your message was invalid and unrecognized.",
            sender
        )
        return "", 204

    # No concat assertion
    if parsing.is_concat(inbound_sms_content):
        texts.send_message(
            "Your message was too long. It was split by your carrier.",
            sender
        )
        return "", 204

    # App availablity
    requested_app = parsing.requested_app(inbound_sms_content)

    if not requested_app:
        texts.send_message(
            f"App '{requested_app}' does not exist.",
            sender
        )
        return "", 204

    # App permissions
    if not parsing.check_permissions(sender, requested_app):
        texts.send_message(
            f"It seems you don't have permission to use app '{requested_app}'.",
            sender
        )
        return "", 204

    # Run the app
    content = parsing.app_content(inbound_sms_content)
    response = requested_app(content)
    texts.send_message(response, sender)

    return "", 204
