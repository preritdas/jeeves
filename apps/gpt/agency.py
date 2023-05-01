"""Agent GPT."""
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback, CallbackManager, StdOutCallbackHandler
from langchain.schema import OutputParserException

import logging  # log agent runs
from logging.handlers import SysLogHandler
from apps.gpt.logging_callback import LoggingCallbackHandler

from keys import KEYS
from apps.gpt import prompts


# ---- Logging ----

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = SysLogHandler(address=(KEYS.Papertrail.host, KEYS.Papertrail.port))
logger.addHandler(handler)

# Log to console and to Papertrail
logging_callback = LoggingCallbackHandler(logger=logger)
callback_manager = CallbackManager([logging_callback, StdOutCallbackHandler()])


# ---- Build the agent ----

class InternalThoughtZeroShotAgent(ZeroShotAgent):
    """
    A normal ZeroShotAgent but doesn't inject "Thought:" before the LLM. AFter testing
    and heavy prompt engineering, I've found a better sucess rate with having the LLM 
    create its own "Thought" label. This is because it knows that each Thought must
    also have either an Action/Action Input or a Final Answer.
    """
    @property
    def llm_prefix(self) -> str:
        """Prefix to append the llm call with."""
        return ""


llm = ChatOpenAI(model_name="gpt-4", openai_api_key=KEYS.OpenAI.api_key, temperature=0)

def create_agent_executor(toolkit: list[Tool]) -> AgentExecutor:
    """Create the agent given authenticated tools."""
    agent_prompts: prompts.AgentPrompts = prompts.build_prompts()
    agent = InternalThoughtZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=toolkit,
        prefix=agent_prompts.prefix,
        format_instructions=agent_prompts.format_instructions,
        suffix=agent_prompts.suffix
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=toolkit,
        verbose=True,
        callback_manager=callback_manager
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
def run_agent(agent_executor: AgentExecutor, query: str) -> str:
    """Run the agent."""
    with get_openai_callback() as cb:
        res = agent_executor.run(query)
        logger.info(
            f"Total Tokens: {cb.total_tokens}, "
            f"Prompt Tokens: {cb.prompt_tokens}, "
            f"Completion Tokens: {cb.completion_tokens}, "
            f"Total Cost (USD): ${cb.total_cost}."
        )
        return res
