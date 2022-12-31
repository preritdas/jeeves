"""GPT applet."""
import utils

from . import completions


APP_HELP = "Get a GPT response."
APP_OPTIONS = {
    "tokens": "Maximum tokens usable in the response. Default is 200."
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    return completions.gpt_response(content, options.get("tokens", 200))
