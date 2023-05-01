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


def generate_agent_response(content: str, inbound_phone: str, uid: str = "") -> str:
    """Build tools, create executor, and run the agent. UID is optional."""
    # UID
    if not uid:
        uid = str(uuid.uuid4())

    callback_handlers = logs_callback.create_callback_handlers(uid)
    toolkit = tool_auth.build_tools(inbound_phone, callback_handlers)
    agent_executor = agency.create_agent_executor(toolkit, callback_handlers)
    response: str = agency.run_agent(agent_executor, content, uid)
    return response.strip()


@utils.app_handler(APP_HELP, OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    if (agency_option := options.get("agency")):
        if agency_option.lower() in {"no", "false", "off"}:
            return completions.gpt_response(content)

    return generate_agent_response(content, options["inbound_phone"])
