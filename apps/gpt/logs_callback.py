"""Create a logging callback handler for the agent."""
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks import CallbackManager, StdOutCallbackHandler

import logging
from logging import Logger
from logging.handlers import SysLogHandler

from typing import Dict, Any, List, Optional, Union
from langchain.schema import LLMResult, AgentAction, AgentFinish

from keys import KEYS
import config


class AgentLoggingCallbackHandler(BaseCallbackHandler):
    """
    Callback Handler that logs instead of printing. 
    Specific for agents, as it uses agent terminology in the logs.
    """
    def __init__(self, logger: Logger) -> None:
        """Initialize callback handler."""
        self.logger = logger

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Do nothing."""
        pass

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Do nothing."""
        pass

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized["name"]
        self.logger.info(f"AgentStart: Entering new {class_name} chain...")
        self.logger.info(f"UserInput: {inputs['input']}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        self.logger.info("AgentFinish: Finished chain.")

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        """Do nothing."""

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        self.logger.info(f"AgentAction: {action.tool}: {action.tool_input}")

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        self.logger.info(f"{observation_prefix}{output}")

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_text(
        self,
        text: str,
        color: Optional[str] = None,
        end: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when agent ends."""
        self.logger.info(text)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        self.logger.info(f"FinalAnswer: {finish.return_values['output']}")


# ---- Logging ----

logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)
handler = SysLogHandler(address=(KEYS.Papertrail.host, KEYS.Papertrail.port))
logger.addHandler(handler)

# Log to console and to Papertrail
logging_callback = AgentLoggingCallbackHandler(logger=logger)
callback_handlers = [logging_callback]

# Log to console as well if configured
if config.GPT.CONSOLE_AGENT:
    callback_handlers.append(StdOutCallbackHandler())

# Create callback manager with all handlers
callback_manager = CallbackManager(callback_handlers)
