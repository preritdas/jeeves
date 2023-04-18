"""GPT applet."""
import utils

from . import agency
from . import tool_auth


APP_HELP = "Get a GPT response."


@utils.app_handler(APP_HELP)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    toolkit = tool_auth.build_tools(options["inbound_phone"])
    agent_executor = agency.create_agent_executor(toolkit)
    response: str = agency.run_agent(agent_executor, content)

    # Remove spaces and newlines from the start of the response
    return response.strip()
