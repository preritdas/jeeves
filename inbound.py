"""
Process and handle inbound requests. This is where the `main_handler` is defined,
called by the Flask route and given inbound information.
"""
import parsing
import permissions
import texts
import usage


def main_handler(inbound_sms_content: dict) -> tuple[str, int]:
    """
    Handle all inbound messages.
    
    Keep this as simple as possible, with plenty of outsourcing.
    """
    sender: str = inbound_sms_content["msisdn"]

    # No concat assertion
    if parsing.is_concat(inbound_sms_content):
        texts.send_message(
            "Your message was too long. It was split by your carrier.",
            sender
        )
        return "", 204

    # Valid assertion
    if not parsing.assert_valid(inbound_sms_content):
        texts.send_message(
            "Your message was invalid and unrecognized.",
            sender
        )
        return "", 204

    # App availablity
    requested_app, app_name = parsing.requested_app(inbound_sms_content)

    if not requested_app:
        texts.send_message(
            f"That app does not exist.",
            sender
        )
        return "", 204

    # App permissions
    if not permissions.check_permissions(sender, app_name):
        texts.send_message(
            f"It seems you don't have permission to use app '{app_name}'.",
            sender
        )
        return "", 204

    # Run the app
    content, options = parsing.app_content_options(inbound_sms_content)
    options["inbound_phone"] = sender

    try:
        response = requested_app(content, options)
    except Exception as e:
        response = f"Unfortunately, that failed. '{str(e)}'"

    texts.send_message(response, sender)
    usage.log_use(
        phone_number = sender,
        app_name = app_name,
        content = content,
        options = options
    ) 

    return "", 204
