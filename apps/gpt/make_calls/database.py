"""Store and retrieve conversations and greetings."""
import deta

from keys import KEYS
import voice_tools as vt


deta_client = deta.Deta(KEYS["Deta"]["project_key"])
convo_base = deta_client.Base("conversations")


class Call:
    """Contains all the relevant information in a call."""
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

        convo_base.update(
            key=self.key,
            updates=updates
        )

    def download(self) -> None:
        """Sync changes from the database to an existing Call object."""
        try:
            call = convo_base.get(self.key)
        except Exception:  # try one more time
            call = convo_base.get(self.key)

        # Update attributes
        self.key = call["key"]
        self.convo = call["convo"]
        self.goal = call["goal"]
        self.recipient_desc = call["recipient_desc"]
        self.greeting = call["greeting"]
        self.greeting_url = call["greeting_url"]


    @classmethod
    def create(cls, goal: str, greeting: str, recipient_desc: str) -> "Call":
        """Create a call."""
        attrs = {
            "convo": "",
            "goal": goal,
            "recipient_desc": recipient_desc,
            "greeting": greeting,
            "greeting_url": vt.speak.speak_jeeves(greeting)
        }

        try:
            key = convo_base.put(data=attrs)["key"]
        except Exception:  # try one more time
            key = convo_base.put(data=attrs)["key"]

        return cls(key=key, **attrs)


    @classmethod
    def from_call_id(cls, call_id: str) -> "Call":
        """Initialize a call object using just a call id."""
        try:
            call = convo_base.get(call_id)
        except Exception:
            call = convo_base.get(call_id)

        return cls(**call)
