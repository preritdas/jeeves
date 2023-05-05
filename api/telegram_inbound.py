"""Routes to handle inbound messages (text and voice) from Telegram."""
from fastapi import APIRouter, Request
import requests

from keys import KEYS

from apps.gpt import generate_agent_response
from voice_tools.transcribe import transcribe_telegram_file_id
from voice_tools.speak import speak_jeeves


router = APIRouter()


async def send_message(user_id: int, message: str):
    """
    Send a message to a Telegram user.
    """
    url = f"https://api.telegram.org/bot{KEYS.Telegram.bot_token}/sendMessage"
    res = requests.post(
        url, 
        data={
            "chat_id": user_id,
            "text": message
        }
    )

    res.raise_for_status()
    return True if res.status_code == 200 else False


async def send_voice_response(user_id: int, message: str):
    """
    Send a voice response to a Telegram user.
    """
    voice_url = speak_jeeves(message, output_format="OGG", output_mime="audio/ogg")

    url = f"https://api.telegram.org/bot{KEYS.Telegram.bot_token}/sendVoice"
    res = requests.post(
        url, 
        data={
            "chat_id": user_id,
            "voice": voice_url
        }
    )

    res.raise_for_status()
    return True if res.status_code == 200 else False


@router.post("/inbound-telegram")
async def handle_inbound_telegram(request: Request) -> str:
    """
    Handle inbound messages from Telegram.

    This is the main handler for inbound Telegram messages. It will receive a request 
    from Telegram, parse the request, and send the message to the appropriate user. 
    If the user is not recognized, it will return a message to the user. If the input 
    type is not recognized, it will return a fail message to the user.
    """
    req = await request.json()
    inbound_id = int(req["message"]["from"]["id"])

    # Get the inbound body
    if "text" in req["message"]:
        inbound_body = req["message"]["text"]
    elif "voice" in req["message"]:
        inbound_body = transcribe_telegram_file_id(req["message"]["voice"]["file_id"])
    else:
        await send_message(inbound_id, "I'm sorry, sir, but I don't understand that yet.")

    # Try to get the phone number from the inbound ID
    recognized_user: str = KEYS.Telegram.id_phone_mapping.get(inbound_id, "")

    # If the user is not recognized, return a message
    if not recognized_user:
        await send_message(
            inbound_id, 
            "My apologies, sir, but it appears I don't recognize you."
        )
        return ""

    # Otherwise, send the message to the recognized user
    response = generate_agent_response(inbound_body, recognized_user)
    await send_message(inbound_id, response)

    # If the response is a voice message, send one back
    if "voice" in req["message"]:
        await send_voice_response(inbound_id, response)

    return ""
