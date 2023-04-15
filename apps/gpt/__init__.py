"""GPT applet."""
import utils

from . import agency


APP_HELP = "Get a GPT response."


@utils.app_handler(APP_HELP)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    response: str = agency.run_agent(content)

    # Remove spaces and newlines from the start of the response
    return response.strip()
