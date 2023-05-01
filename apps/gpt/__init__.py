"""GPT applet."""
import utils

import uuid

from apps.gpt import agency
from apps.gpt import tool_auth
from apps.gpt import completions
from apps.gpt import logs_callback


APP_HELP = "Speak with Jeeves."
OPTIONS = {
    "agency": "'no' if you want a basic GPT response, not Jeeves."
}


@utils.app_handler(APP_HELP, OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    if (agency_option := options.get("agency")):
        if agency_option.lower() in {"no", "false", "off"}:
            return completions.gpt_response(content)

    uid = str(uuid.uuid4())
    callback_manager = logs_callback.create_callback_manager(uid)
    toolkit = tool_auth.build_tools(options["inbound_phone"], callback_manager)
    agent_executor = agency.create_agent_executor(toolkit, callback_manager)
    response: str = agency.run_agent(agent_executor, content, uid)

    # Remove spaces and newlines from the start of the response
    return response.strip()
