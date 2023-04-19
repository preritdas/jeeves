"""Agent GPT."""
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

from keys import KEYS


# Context to the agent
PREFIX = r"""You are Jeeves, my gentleman's gentleman. 
You always respond in the colloquial and over-the-top tone that Jeeves uses in the Woodhouse novels.
Always address me as sir.

Answer the following questions as best you can. You have access to the following tools:"""

FORMAT_INSTRUCTIONS = r"""If you're sending a message externally 
(ex. email, Teams, Discord) you must introduce yourself (just your name) before the message content.
Also, if sending a message externally, include the exact content of the message you sent
in your final answer.

Use the following format:

Question: the input question you must answer thoroughly, with detail
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the thorough, detailed final answer to the original input question

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


llm = ChatOpenAI(model_name="gpt-4", openai_api_key=KEYS["OpenAI"]["api_key"], temperature=0)

def create_agent_executor(toolkit: list[Tool]) -> AgentExecutor:
    """Create the agent given authenticated tools."""
    agent = ZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=toolkit,
        prefix=PREFIX,
        format_instructions=FORMAT_INSTRUCTIONS
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=toolkit,
        verbose=True
    )


def retry_couldnt_parse(function):
    """Decorator to retry up to three times if a specific ValueError occurs."""
    def wrapper(*args, **kwargs):
        retries = 0
        last_exception = None
        while retries < 3:
            try:
                return function(*args, **kwargs)
            except ValueError as e:
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
