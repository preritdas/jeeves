"""Store and retrieve conversations and greetings."""
import deta

from jeeves.keys import KEYS
from jeeves import voice_tools as vt

from jeeves.applets.gpt.make_calls.prompts import generate_intro_message


deta_client = deta.Deta(KEYS.Deta.project_key)
convo_base = deta_client.Base("conversations")


class Call:
    """
    Contains all the relevant information in a call.
    Provides an interface for creating, updating,
    and downloading call attributes from the conversations
    database. This way, only one Deta API call is required
    per API route.
    """
    def __init__(
        self,
        key: str,
        convo: str,
        goal: str,
        recipient_desc: str,
        greeting: str,
        greeting_url: str
    ) -> None:
        self.key = key
        self.convo = convo
        self.goal = goal
        self.recipient_desc = recipient_desc
        self.greeting = greeting
        self.greeting_url = greeting_url

    def upload(self) -> None:
        """Update the call record in Deta."""
        updates = self.__dict__.copy()
        del updates["key"]

        convo_base.update(key=self.key, updates=updates)

    def download(self) -> None:
        """Sync changes from the database to an existing Call object."""
        try:
            call = convo_base.get(self.key)
        except Exception:  # try one more time
            call = convo_base.get(self.key)

        # Update all attributes
        self.__dict__.update(call)

    @classmethod
    def create(cls, goal: str, recipient_desc: str) -> "Call":
        """Create a call."""
        # Create the greeting
        greeting = generate_intro_message(goal, recipient_desc)

        attrs = {
            "convo": "",
            "goal": goal,
            "recipient_desc": recipient_desc,
            "greeting": greeting,
            "greeting_url": vt.speak.speak_jeeves(greeting)
        }

        try:
            call = convo_base.put(data=attrs)
        except Exception:  # try one more time
            call = convo_base.put(data=attrs)

        # Call is a dictionary of the newly added item
        return cls(**call)

    @classmethod
    def from_call_id(cls, call_id: str) -> "Call":
        """Initialize a call object using just a call id."""
        try:
            call = convo_base.get(call_id)
        except Exception:
            call = convo_base.get(call_id)

        return cls(**call)

    def delete(self) -> None:
        """Delete the call record from the database."""
        convo_base.delete(self.key)
