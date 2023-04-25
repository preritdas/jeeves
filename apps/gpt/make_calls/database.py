"""Store and retrieve conversations and greetings."""
import deta

from keys import KEYS
import voice_tools as vt


deta_client = deta.Deta(KEYS["Deta"]["project_key"])
convo_base = deta_client.Base("conversations")
greetings_base = deta_client.Base("greetings")


def create_call(goal: str, greeting: str) -> str:
    """Creates a call and returns a call ID."""
    key = convo_base.put({"convo": ""})["key"]
    greetings_base.put(
        {
            "goal": goal, 
            "greeting": greeting,
            "greeting_url": vt.speak.speak_jeeves(greeting)
        },
        key=key
    )
    return key


def decode_greeting(call_id: str) -> str:
    """Uses ID to find greeting."""
    res = greetings_base.get(call_id)["greeting"]
    return res


def decode_greeting_url(call_id: str) -> str:
    """Uses ID to find greeting."""
    res = greetings_base.get(call_id)["greeting_url"]
    return res


def decode_goal(call_id: str) -> str:
    """Uses ID to find goal."""
    res = greetings_base.get(call_id)["goal"]
    return res


def encode_convo(call_id: str, convo: str) -> None:
    """Stores and returns ID."""
    convo_base.update({"convo": convo}, key=call_id)


def decode_convo(call_id: str) -> str:
    """Uses ID to find convo."""
    res = convo_base.get(call_id)["convo"]
    return res
