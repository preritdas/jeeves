"""Agent GPT."""
from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper

import keys


toolkit = [
    Tool(
        name="Google Search",
        func=GoogleSerperAPIWrapper(serper_api_key=keys.GoogleSerper.API_KEY).run,
        description="Useful for when you need to search Google."
    )
]

llm = ChatOpenAI(model_name="gpt-4", openai_api_key=keys.OpenAI.API_KEY, temperature=0)
agent = initialize_agent(toolkit, llm)


def retry_couldnt_parse(function):
    """Decorator to retry three times if the agent couldn't parse the output."""
    def wrapper(*args, **kwargs):
        for _ in range(3):
            try:
                return function(*args, **kwargs)
            except ValueError as e:
                if "Could not parse LLM output" in str(e):
                    continue
                raise e
    return wrapper


@retry_couldnt_parse
def run_agent(query: str) -> str:
    """Run the agent."""
    agent.run(query)
