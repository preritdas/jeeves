"""Agent GPT."""
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import OutputParserException

import uuid
import pytz
import datetime as dt

from jeeves.keys import KEYS
from jeeves.config import CONFIG

from jeeves.agency import tool_auth
from jeeves.agency.chat_history.models import Message
from jeeves.agency import logs_callback, prompts
from jeeves.agency.chat_history import ChatHistory, RecencyFilterer


# ---- Build the agent ----

class InternalThoughtZeroShotAgent(ZeroShotAgent):
    """
    A normal ZeroShotAgent but doesn't inject "Thought:" before the LLM. After testing
    and heavy prompt engineering, I've found a better sucess rate with having the LLM
    create its own "Thought" label. This is because it knows that each Thought must
    also have either an Action/Action Input or a Final Answer.
    """
    @property
    def llm_prefix(self) -> str:
        """Prefix to append the llm call with."""
        return ""


llm = ChatOpenAI(model_name="gpt-4", openai_api_key=KEYS.OpenAI.api_key, temperature=0)

def create_agent_executor(
    toolkit: list[Tool],
    chat_history: ChatHistory,
    callback_handlers: list[BaseCallbackHandler],
) -> AgentExecutor:
    """Create the agent given authenticated tools."""
    agent_prompts: prompts.AgentPrompts = prompts.build_prompts(
        chat_history=chat_history.format_messages(
            filterer=RecencyFilterer(n_messages=5)
        )
    )
    agent = InternalThoughtZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=toolkit,
        prefix=agent_prompts.prefix,
        format_instructions=agent_prompts.format_instructions,
        suffix=agent_prompts.suffix
    )
    return AgentExecutor(
        agent=agent, tools=toolkit, verbose=True, callbacks=callback_handlers
    )


# ---- Run the agent ----

def retry_couldnt_parse(function):
    """Decorator to retry up to three times if a specific ValueError occurs."""
    def wrapper(*args, **kwargs):
        retries = 0
        last_exception = None
        while retries < 3:
            try:
                return function(*args, **kwargs)
            except OutputParserException as e:
                if "Could not parse LLM output" in str(e):
                    retries += 1
                    last_exception = e
                else:
                    raise e
        raise last_exception

    return wrapper


@retry_couldnt_parse
def run_agent(agent_executor: AgentExecutor, query: str, uid: str) -> str:
    """Run the agent."""
    with get_openai_callback() as cb:
        res = agent_executor.run(query)
        logs_callback.logger.info(
            f"{uid}: UsageInfo: "
            f"Total Tokens: {cb.total_tokens}, "
            f"Prompt Tokens: {cb.prompt_tokens}, "
            f"Completion Tokens: {cb.completion_tokens}, "
            f"Total Cost (USD): ${cb.total_cost:.2f}."
        )
        return res


def generate_agent_response(content: str, inbound_phone: str, uid: str = "") -> str:
    """Build tools, create executor, and run the agent. UID is optional."""
    # UID
    if not uid:
        uid = str(uuid.uuid4())

    # Build chat history and toolkit using inbound phone
    chat_history = ChatHistory.from_inbound_phone(inbound_phone)
    toolkit = tool_auth.build_tools(inbound_phone, callback_handlers)

    # Run
    callback_handlers = logs_callback.create_callback_handlers(uid)
    agent_executor = create_agent_executor(
        toolkit, chat_history, callback_handlers
    )
    response: str = run_agent(agent_executor, content, uid)

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