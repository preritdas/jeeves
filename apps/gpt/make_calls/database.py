"""Store and retrieve conversations and greetings."""
import deta

from keys import KEYS


deta_client = deta.Deta(KEYS["Deta"]["project_key"])
convo_base = deta_client.Base("conversations")
greetings_base = deta_client.Base("greetings")


def encode_greeting(greeting: str) -> str:
    """Stores and returns ID."""
    res = greetings_base.put({"greeting": greeting})
    return res["key"]


def decode_greeting(greeting_id: str) -> str:
    """Uses ID to find greeting."""
    res = greetings_base.get(greeting_id)["greeting"]
    return res


def encode_convo(convo: str) -> str:
    """Stores and returns ID."""
    res = convo_base.put({"convo": convo})
    return res["key"]


def decode_convo(convo_id: str) -> str:
    """Uses ID to find convo."""
    res = convo_base.get(convo_id)["convo"]
    return res
