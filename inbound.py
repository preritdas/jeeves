"""
Process and handle inbound requests. This is where the `main_handler` is defined,
called by the FastAPI route and given inbound information.
"""
import parsing
import permissions
import texts
import usage


def main_handler(inbound_sms_content: parsing.InboundMessage) -> dict[str, tuple | str]:
    """
    Handle all inbound messages. Returns a dictionary in the following format.

    {
        "response": "That app does not exist."  # what's texted to the user
        "http": ("", 204)  # what's returned (not actually) by HTTP
    }
    
    Keep this as simple as possible, with plenty of outsourcing.
    """
    sender: str = inbound_sms_content.phone_number
    respond = lambda response: texts.send_message(response, sender)

    # Valid assertion
    if not parsing.assert_valid(inbound_sms_content):
        text_response = "Your message was invalid and unrecognized."
        respond(text_response)
        return {"response": text_response, "http": ("", 204)}

    # App availablity
    requested_app, app_name = parsing.requested_app(inbound_sms_content)

    if not requested_app:
        text_response = f"That app does not exist."
        respond(text_response)
        return {"response": text_response, "http": ("", 204)}

    # App permissions
    if not permissions.check_permissions(sender, app_name):
        text_response = f"It seems you don't have permission to use app '{app_name}'."
        respond(text_response)
        return {"response": text_response, "http": ("", 204)}

    # Run the app
    content, options = parsing.app_content_options(inbound_sms_content)
    options["inbound_phone"] = sender

    try:
        text_response = requested_app(content, options)
    except Exception as e:
        text_response = f"Unfortunately, that failed. '{str(e)}'"

    respond(text_response)
    usage.log_use(
        phone_number = sender,
        app_name = app_name,
        content = content,
        options = options
    ) 

    return {"response": text_response, "http": ("", 204)}
