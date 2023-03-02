"""GPT applet."""
import utils

from . import completions


APP_HELP = "Get a GPT response."


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    response: str = completions.gpt_response(content)

    # Remove newlines from the start of the response
    while response.startswith("\n"):
        response = response[1:]

    return response
