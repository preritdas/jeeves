"""Store and retrieve conversations and greetings."""
import deta

from keys import KEYS
import voice_tools as vt


deta_client = deta.Deta(KEYS["Deta"]["project_key"])
convo_base = deta_client.Base("conversations")


def create_call(goal: str, greeting: str, recipient_desc: str) -> str:
    """Creates a call and returns a call ID."""
    conversation = convo_base.put(
        {
            "convo": "",
            "goal": goal,
            "recipient_desc": recipient_desc,
            "greeting": greeting,
            "greeting_url": vt.speak.speak_jeeves(greeting)
        }
    )

    return conversation["key"]


def decode_greeting(call_id: str) -> str:
    """Uses ID to find greeting."""
    res = convo_base.get(call_id)["greeting"]
    return res


def decode_greeting_url(call_id: str) -> str:
    """Uses ID to find greeting."""
    res = convo_base.get(call_id)["greeting_url"]
    return res


def decode_goal(call_id: str) -> str:
    """Uses ID to find goal."""
    res = convo_base.get(call_id)["goal"]
    return res


def decode_recipient_desc(call_id: str) -> str:
    """Uses ID to find recipient description."""
    res = convo_base.get(call_id)["recipient_desc"]
    return res


def encode_convo(call_id: str, convo: str) -> None:
    """Stores and returns ID."""
    convo_base.update({"convo": convo}, key=call_id)


def decode_convo(call_id: str) -> str:
    """Uses ID to find convo."""
    res = convo_base.get(call_id)["convo"]
    return res
