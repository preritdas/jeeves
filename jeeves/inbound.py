"""
Process and handle inbound requests. This is where the `main_handler` is defined,
called by the FastAPI route and given inbound information.
"""
from jeeves import parsing
from jeeves import permissions
from jeeves import texts
from jeeves import usage


def main_handler(
    inbound_message: parsing.InboundMessage, send_response_message: bool = True
) -> dict[str, tuple | str]:
    """
    Handle all inbound messages. Returns a dictionary in the following format.

    {
        "response": "That app does not exist."  # what's texted to the user
        "http": ("", 204)  # what's returned (not actually) by HTTP
    }

    Keep this as simple as possible, with plenty of outsourcing.
    """
    sender: str = inbound_message.phone_number

    # Define the response action based on whether or not we want to send a response
    respond = lambda response: None if not send_response_message \
        else texts.send_message(response, sender)

    # App availablity
    requested_app, app_name = inbound_message.requested_app

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
    content, options = inbound_message.app_content_options
    options["inbound_phone"] = sender

    try:
        text_response = requested_app(content, options)
    except Exception as e:
        text_response = f"Unfortunately, that failed. '{str(e)}'"

    respond(text_response)
    usage.log_use(
        phone_number=sender, app_name=app_name, content=content, options=options
    )

    return {"response": text_response, "http": ("", 204)}
