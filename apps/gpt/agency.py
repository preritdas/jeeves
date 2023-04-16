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


def run_agent(query: str) -> str:
    """Run the agent."""
    return agent.run(query)
