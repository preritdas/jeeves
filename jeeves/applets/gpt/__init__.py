"""Interface for speaking with Jeeves as an applet."""
from jeeves import utils
from jeeves.permissions import User

from jeeves.agency import generate_agent_response
from jeeves.applets.gpt import completions

APP_HELP = "Speak with Jeeves."
OPTIONS = {"agency": "'no' if you want a basic GPT response, not Jeeves."}


@utils.app_handler(APP_HELP, OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    if agency_option := options.get("agency"):
        if agency_option.lower() in {"no", "false", "off"}:
            return completions.gpt_response(content)

    user = User.from_phone(options["inbound_phone"])
    return generate_agent_response(content, user)
