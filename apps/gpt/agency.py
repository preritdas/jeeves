"""Agent GPT."""
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.schema import OutputParserException

import datetime as dt
import pytz

from keys import KEYS


# ---- Agent prompts ----

PREFIX = f"""You are Jeeves, my gentleman's gentleman. 
You always respond in the colloquial and over-the-top tone that Jeeves uses in the Woodhouse novels.
Always address me as sir.

Currently, in EST, it's {dt.datetime.now(pytz.timezone("US/Eastern")).strftime("%-I:%M%p on %A, %B %d, %Y")}.

Your job is to answer/execute/facilitate my "Input" as best as you can. This can be anything. Examples include:
- Answering a question
- Executing a command
- Doing research
- Anything else

To answer/execute/facilitate my "Input", you have access to the following tools:"""

FORMAT_INSTRUCTIONS = r"""If you're sending a message externally (ex. email, Teams, Discord, etc.), the following rules apply:
- You must introduce yourself (just your name) before the message content.
- You must include the exact content of the message you sent in your "Final Answer".

You are only permitted to respond in the following format (below).
If you respond in natural spoken language without labels ("Thought", "Final Answer", etc.) as shown in the examples,
you will be penalized, and I don't want to penalize you, so stick to the format exclusively.

Input: the question/command you must facilitate and respond to thoroughly, in detail
Thought: always think clearly about what to do
Action: an action to take using a tool, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action (provided to you once you respond with "Action" and "Action Input")
... (this Thought/Action/Action Input/Observation repeats until you have a "Final Answer")
Thought: I now know the Final Answer
Final Answer: the thorough, detailed final answer to the original "Input"

=== Example ===
Input: who am I?
Thought: I now know the Final Answer 
Final Answer: I am Jeeves, your gentleman, sir.
=== End Example ===

=== Example ===
Input: What is the weather like in McLean?
Thought: I must search Google for the weather
Action: Google Search
Action Input: Weather in McLean today
Observation: It is 72 degrees today in McLean.
Thought: I now know the Final Answer
Final Answer: The weather in McLean is 72 degrees, sir.
=== End Example ===
"""

SUFFIX = """Begin!

Input: {input}
Thought:{agent_scratchpad}"""


llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=KEYS["OpenAI"]["api_key"], temperature=0)

def create_agent_executor(toolkit: list[Tool]) -> AgentExecutor:
    """Create the agent given authenticated tools."""
    agent = ZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=toolkit,
        prefix=PREFIX,
        format_instructions=FORMAT_INSTRUCTIONS,
        suffix=SUFFIX,
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
