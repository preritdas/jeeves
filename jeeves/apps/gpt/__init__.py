"""GPT applet."""
from jeeves import utils

import uuid
import datetime as dt
import pytz

from jeeves.config import CONFIG

from jeeves.apps.gpt import agency
from jeeves.apps.gpt import tool_auth
from jeeves.apps.gpt import completions
from jeeves.apps.gpt import logs_callback

from jeeves.apps.gpt.chat_history import ChatHistory
from jeeves.apps.gpt.chat_history.models import Message


APP_HELP = "Speak with Jeeves."
OPTIONS = {"agency": "'no' if you want a basic GPT response, not Jeeves."}


def generate_agent_response(content: str, inbound_phone: str, uid: str = "") -> str:
    """Build tools, create executor, and run the agent. UID is optional."""
    # UID
    if not uid:
        uid = str(uuid.uuid4())

    # Build chat history
    chat_history = ChatHistory.from_inbound_phone(inbound_phone)

    callback_handlers = logs_callback.create_callback_handlers(uid)
    toolkit = tool_auth.build_tools(inbound_phone, callback_handlers)
    agent_executor = agency.create_agent_executor(
        toolkit, chat_history, callback_handlers
    )
    response: str = agency.run_agent(agent_executor, content, uid)

    # Save message to chats database
    chat_history.add_message(
        Message(
            datetime=dt.datetime.now(pytz.timezone(CONFIG.General.default_timezone)),
            inbound_phone=inbound_phone,
            user_input=content,
            agent_response=response
        )
    )

    return response.strip()


@utils.app_handler(APP_HELP, OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the GPT applet."""
    if agency_option := options.get("agency"):
        if agency_option.lower() in {"no", "false", "off"}:
            return completions.gpt_response(content)

    return generate_agent_response(content, options["inbound_phone"])
