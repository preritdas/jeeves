"""Routes to handle inbound messages (text and voice) from Telegram."""
from fastapi import APIRouter, Request
import requests

from threading import Thread

from keys import KEYS
from apps.gpt import generate_agent_response
from voice_tools.transcribe import transcribe_telegram_file_id
from voice_tools.speak import speak_jeeves


router = APIRouter()


def send_message(user_id: int, message: str):
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


def send_voice_response(user_id: int, message: str):
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


def process_telegram_inbound(inbound_id: int, text: str = "", voice_id: str = "") -> None:
    """
    Process an inbound message from Telegram. 

    This is the main handler for inbound Telegram messages. It will receive a request 
    from Telegram, parse the request, and send the message to the appropriate user. 
    If the user is not recognized, it will return a message to the user. If the input 
    type is not recognized, it will return a fail message to the user.
    """
    # Check for proper usage
    if text and voice_id:
        raise ValueError("You can only provide text or voice, not both.")
    elif not text and not voice_id:
        raise ValueError("You must provide either text or voice.")
    
    # Try to get the phone number from the inbound ID
    recognized_user: str = KEYS.Telegram.id_phone_mapping.get(inbound_id, "")

    # If the user is not recognized, return a message
    if not recognized_user:
        send_message(
            inbound_id, 
            "My apologies, sir, but it appears I don't recognize you."
        )
        return
    
    # Otherwise, send the message to the recognized user
    text = text or transcribe_telegram_file_id(voice_id)
    
    # Generate and catch errors
    try: 
        response = generate_agent_response(text, recognized_user)
    except Exception as e:
        response = f"Unfortunately, that failed. {e}"
    
    # Text reply regardless of input type
    send_message(inbound_id, response)

    # If the response is a voice message, send one back
    if voice_id:
        send_voice_response(inbound_id, response)

    return


@router.post("/inbound-telegram")
async def handle_inbound_telegram(request: Request) -> str:
    """
    Handle inbound messages from Telegram.
    """
    req = await request.json()
    inbound_id = int(req["message"]["from"]["id"])

    process_kwargs = {"inbound_id": inbound_id}

    # Get the inbound body
    if "text" in req["message"]:
        process_kwargs["text"] = req["message"]["text"]
    elif "voice" in req["message"]:
        process_kwargs["voice_id"] = req["message"]["voice"]["file_id"]
    else:
        send_message(inbound_id, "I'm sorry, sir, but I don't understand that yet.")
        return ""

    # Process the inbound message in a thread
    process_thread = Thread(
        target=process_telegram_inbound,
        kwargs=process_kwargs
    )

    process_thread.start()
    return ""
