"""Routes to handle inbound messages (text and voice) from Telegram."""
from fastapi import APIRouter, Request, Response
import requests

from threading import Thread

from api.verification import validate_telegram_request

from jeeves.keys import KEYS
from jeeves.config import CONFIG
from jeeves.permissions import User

from jeeves.agency import generate_agent_response
from jeeves.voice_tools.transcribe import transcribe_telegram_file_id
from jeeves.voice_tools.speak import speak_jeeves


# Create the main router for Telegram operations
router = APIRouter()


def send_message(user_id: int, message: str, reply_id: int | None = None) -> bool:
    """
    Send a message to a Telegram user as a reply to a message.
    """
    if CONFIG.General.sandbox_mode:
        return True

    payload = {
        "chat_id": user_id, 
        "text": message, 
        "reply_to_message_id": reply_id
    }

    if reply_id:
        payload["reply_to_message_id"] = reply_id

    url = f"https://api.telegram.org/bot{KEYS.Telegram.bot_token}/sendMessage"
    res = requests.post(url, data=payload)

    res.raise_for_status()
    return True if res.status_code == 200 else False


def send_voice_response(user_id: int, message: str, reply_id: int):
    """
    Send a voice response to a Telegram user as a reply to a message.
    """
    if CONFIG.General.sandbox_mode:
        return True

    voice_url = speak_jeeves(message, output_format="OGG", output_mime="audio/ogg")

    url = f"https://api.telegram.org/bot{KEYS.Telegram.bot_token}/sendVoice"
    res = requests.post(
        url, 
        data={
            "chat_id": user_id, 
            "voice": voice_url,
            "reply_to_message_id": reply_id
        }
    )

    res.raise_for_status()
    return True if res.status_code == 200 else False


def process_telegram_inbound(
    inbound_id: int, reply_id: int, text: str = "", voice_id: str = ""
) -> str:
    """
    Process an inbound message from Telegram.

    This is the main handler for inbound Telegram messages. It will receive a request
    from Telegram, parse the request, and send the message to the appropriate user as 
    a reply to the user's inbound message. If the user is not recognized, it will 
    return a message to the user. If the input type is not recognized, it will return 
    a failure message to the user.
    """
    # Check for proper usage
    if text and voice_id:
        raise ValueError("You can only provide text or voice, not both.")
    elif not text and not voice_id:
        raise ValueError("You must provide either text or voice.")

    # Try to get the phone number from the inbound ID
    user: User | None = User.from_telegram_id(inbound_id)

    # If the user is not recognized, return a message
    if not user:
        response = (
            "My apologies, but it appears I don't recognize you. "
            f"Your telegram ID is {inbound_id}."
        )
        send_message(inbound_id, response, reply_id)
        return response

    # Otherwise, send the message to the recognized user
    text = text or transcribe_telegram_file_id(voice_id)

    # Generate and catch errors
    try:
        response = generate_agent_response(text, user)
    except Exception as e:
        response = f"Unfortunately, that failed. {e}"

    # Text reply regardless of input type
    send_message(inbound_id, response, reply_id)

    # If the response is a voice message, send one back
    if voice_id and CONFIG.Telegram.voice_note_responses:
        send_voice_response(inbound_id, response, reply_id)

    return response


@router.post("/inbound-telegram")
async def handle_inbound_telegram(request: Request) -> str:
    """
    Handle inbound messages from Telegram.
    """
    # Validate the request
    if not await validate_telegram_request(request):
        return Response(status_code=401)

    req = await request.json()

    # If unprocessable update (for now)
    if "message" not in req:
        return ""

    # Get the inbound ID of the user
    inbound_id = int(req["message"]["from"]["id"])
    reply_id = int(req["message"]["message_id"])
    process_kwargs = {"inbound_id": inbound_id, "reply_id": reply_id}

    # Get the inbound body
    if "text" in req["message"]:
        process_kwargs["text"] = req["message"]["text"]
    elif "voice" in req["message"]:
        process_kwargs["voice_id"] = req["message"]["voice"]["file_id"]
    else:
        send_message(inbound_id, "I'm sorry, sir, but I don't understand that yet.")
        return ""

    # Don't process the inbound message in a thread if configured
    if not CONFIG.Telegram.threaded_inbound:
        process_telegram_inbound(**process_kwargs)
        return ""

    # Otherwise, process in a thread
    process_thread = Thread(target=process_telegram_inbound, kwargs=process_kwargs)
    process_thread.start()
    return ""
