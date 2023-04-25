"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response
from twilio.twiml.voice_response import VoiceResponse
import deta

from urllib.parse import urlencode

from . import prompts
from keys import KEYS


router = APIRouter()
convo_base = deta.Deta(KEYS["Deta"]["project_key"]).Base("conversations")



def encode_convo(convo: str) -> str:
    """Stores and returns ID."""
    res = convo_base.put({"convo": convo})
    return res["key"]


def decode_convo(convo_id: str) -> str:
    """Uses ID to find convo."""
    res = convo_base.get(convo_id)["convo"]
    return res


@router.post("/handler")
async def handler(request: Request, goal: str, convo_id: str = None):
    twiml = VoiceResponse()
    send_to_respond: dict[str, str] = {"goal": goal}

    if convo_id:
        send_to_respond["convo_id"] = convo_id

    intro_message: str = prompts.generate_intro_message(goal),
  
    # If no previous conversation is present, start the conversation
    if not convo:
        twiml.say(
            intro_message,
            voice="Polly.Joanna-Neural"
        )
        convo = f"AI: {intro_message}"
        send_to_respond["convo_id"] = encode_convo(convo)

    # Listen to user response and pass input to /respond
    twiml.gather(
        enhanced=True,
        speech_timeout="auto",
        speech_model="phone_call",
        input="speech",
        action=f"/voice/outbound/respond?{urlencode(send_to_respond)}",
    )

    return Response(twiml.to_xml(), media_type='text/xml')


@router.post("/respond")
async def respond(request: Request, goal: str, convo_id: str = None):
    twiml = VoiceResponse()
    send_to_handler: dict[str, str] = {"goal": goal}

    # Grab previous conversations and the user's voice input from the request
    event = await request.form()
    voice_input = event["SpeechResult"]

    # Format input for GPT-3 and voice the response
    if convo_id:
        convo = decode_convo(convo_id)
    else:
        convo = ""

    convo += f"\nRecipient: {voice_input}\nAI: "
    ai_response = prompts.generate_response(goal, convo)
    convo += ai_response
    twiml.say(
        ai_response,
        voice="Polly.Joanna-Neural"
    )

    # Pass new convo back to /handler
    send_to_handler["convo_id"] = encode_convo(convo)
    twiml.redirect(
        f"/voice/outbound/handler?{urlencode(send_to_handler)}",
        method="POST"
    )

    return Response(twiml.to_xml(), media_type='text/xml')
