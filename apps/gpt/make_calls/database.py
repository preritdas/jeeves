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

    def update(self) -> None:
        """Update the call record in Deta."""
        updates = self.__dict__.copy()
        del updates["key"]

        convo_base.update(
            key=self.key,
            updates=updates
        )

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
        key = convo_base.put(data=attrs)["key"]
        return cls(key=key, **attrs)


    @classmethod
    def from_call_id(cls, call_id: str) -> "Call":
        """Initialize a call object using just a call id."""
        call = convo_base.get(call_id)
        return cls(**call)
