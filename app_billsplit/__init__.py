"""Split the bill and vote on tip."""
import utils

from . import actions


APP_HELP = (
    "Split the bill and vote on the tip. This app is in beta. "
    "If you're participating, provide the phrase as an option and "
    "your suggested tip as content. If you're creating a session, "
    "use the create action, specify the total as an option, and your suggested "
    "tip as content."
)
APP_OPTIONS = {
    "phrase": "Unique phrase provided by creator.",
    "action": "'start' to initiate the split, " \
        "'status' to check on the status, 'close' to make everyone pay.",
    "total": "If creating, the total value of the bill, without tip."
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the bill split app."""
    if options.get("action") == "start":
        if not "total" in options:
            return "You must supply a total."

        try:
            total = float(options["total"])
        except ValueError:
            return "Invalid total."
        
        if not content:
            return "You must supply a suggested tip as content."

        try:
            tip = float(content)
        except ValueError:
            return "Invalid tip."

        return actions.create_session(options["inbound_phone"], total, tip)

    if options.get("action") == "status":
        if not content:
            return "You must provide the unique phrase as content."

        return actions.status(content)

    if options.get("action") == "close":
        if not content:
            return "When closing, provide the phrase as content."

        return actions.close(options["inbound_phone"], content)

    # Participating
    if not "phrase" in options:
        return "As a participant, you must specify the unique phrase as an option."

    try:
        tip = float(content)
    except ValueError:
        return "Invalid tip."

    return actions.participate(options["inbound_phone"], options["phrase"], tip)
