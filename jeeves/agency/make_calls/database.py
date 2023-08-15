"""Store and retrieve conversations and greetings."""
from pymongo import MongoClient
from bson.objectid import ObjectId

from jeeves.keys import KEYS
from jeeves import voice_tools as vt

from jeeves.agency.make_calls.prompts import generate_intro_message


# Connect to the database collection
CONVERSATIONS_COLL = MongoClient(KEYS.MongoDB.connect_str)["Jeeves"]["conversations"]


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
        """Initialize a call object."""
        self.key = key
        self._id = ObjectId(key)
        self.convo = convo
        self.goal = goal
        self.recipient_desc = recipient_desc
        self.greeting = greeting
        self.greeting_url = greeting_url

    def upload(self) -> None:
        """Update the call record in Deta."""
        updates = self.__dict__.copy()
        del updates["_id"]
        del updates["key"]

        CONVERSATIONS_COLL.update_one({"_id": self._id}, updates)

    def download(self) -> None:
        """Sync changes from the database to an existing Call object."""
        call = CONVERSATIONS_COLL.find_one({"_id": self._id})

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

        _id = CONVERSATIONS_COLL.insert_one(attrs).inserted_id

        # Call is a dictionary of the newly added item
        return cls(key=str(_id), **attrs)

    @classmethod
    def from_call_id(cls, call_id: str) -> "Call":
        """Initialize a call object using just a call id."""
        call = CONVERSATIONS_COLL.find_one({"_id": ObjectId(call_id)})
        return cls(**call)

    def delete(self) -> None:
        """Delete the call record from the database."""
        CONVERSATIONS_COLL.delete_one({"_id": self._id})
