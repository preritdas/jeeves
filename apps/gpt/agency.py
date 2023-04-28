"""Agent GPT."""
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.schema import OutputParserException

from keys import KEYS
from . import prompts


# ---- Build the agent ----

llm = ChatOpenAI(model_name="gpt-4", openai_api_key=KEYS["OpenAI"]["api_key"], temperature=0)

def create_agent_executor(toolkit: list[Tool]) -> AgentExecutor:
    """Create the agent given authenticated tools."""
    agent_prompts: prompts.AgentPrompts = prompts.build_prompts()
    agent = ZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=toolkit,
        prefix=agent_prompts.prefix,
        format_instructions=agent_prompts.format_instructions,
        suffix=agent_prompts.suffix
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=toolkit,
        verbose=True
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
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")    
        return res
