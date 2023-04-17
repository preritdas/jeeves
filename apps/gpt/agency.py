"""Agent GPT."""
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper

import keys

from . import retrieval


# Context to the agent
PREFIX = r"""You are Jeeves, my gentleman's gentleman. 
You always respond in the colloquial and over-the-top tone that Jeeves uses in the Woodhouse novels.
Always address me as sir.

Answer the following questions as best you can. You have access to the following tools:"""

FORMAT_INSTRUCTIONS = r"""Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

=== Example ===
Question: who am I?
Thought: I now know the final answer
Final Answer: I am Jeeves, sir.
=== End Example ===

=== Example ===
Question: What is the weather like in McLean?
Thought: I must search Google for the weather
Action: Google Search
Action Input: Weather in McLean today
Observation: It is 72 degrees today in McLean.
Thought: I now know the final answer
Final Answer: The weather in McLean is 72 degrees, sir.
=== End Example ===
"""

JSON_STRING_INPUT_INSTRUCTIONS = "Input must be a JSON string with the keys \"source\" and \"query\"."

toolkit = [
    Tool(
        name="Google Search",
        func=GoogleSerperAPIWrapper(serper_api_key=keys.GoogleSerper.API_KEY).run,
        description="Useful for when you need to search Google."
    ),
    Tool(
        name="Website Answerer",
        func=retrieval.WebsiteAnswerer.answer_json_string,
        description=(
            "Useful for when you need to answer a question about the content on a website. "
            f"{JSON_STRING_INPUT_INSTRUCTIONS} \"source\" is the URL of the website."
        )
    )
]

llm = ChatOpenAI(model_name="gpt-4", openai_api_key=keys.OpenAI.API_KEY, temperature=0)
agent = ZeroShotAgent.from_llm_and_tools(
    llm=llm,
    tools=toolkit,
    prefix=PREFIX,
    format_instructions=FORMAT_INSTRUCTIONS
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=toolkit,
    verbose=True
)


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
        
        raise e  # if it never worked
    return wrapper


@retry_couldnt_parse
def run_agent(query: str) -> str:
    """Run the agent."""
    return agent_executor.run(query)
