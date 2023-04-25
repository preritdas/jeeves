"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response
from twilio.twiml.voice_response import VoiceResponse
import deta

from urllib.parse import urlencode

from . import prompts
from keys import KEYS


router = APIRouter()
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


@router.post("/handler")
async def handler(request: Request, goal: str, greeting_id: str = None, convo_id: str = None):
    twiml = VoiceResponse()
    send_to_respond: dict[str, str] = {"goal": goal}
  
    # If no previous conversation is present, start the conversation
    if not convo_id and greeting_id:
        intro_message: str = prompts.generate_intro_message(goal)

        twiml.say(
            decode_greeting(greeting_id),
            voice="Polly.Joanna-Neural"
        )
        convo = f"AI: {intro_message}"
        send_to_respond["convo_id"] = encode_convo(convo)

    if convo_id:
        send_to_respond["convo_id"] = convo_id

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

    # If we need to hangup
    if "HANGUP" in ai_response:
        return Response(VoiceResponse().hangup().to_xml(), media_type='text/xml')

    # Pass new convo back to /handler
    send_to_handler["convo_id"] = encode_convo(convo)
    twiml.redirect(
        f"/voice/outbound/handler?{urlencode(send_to_handler)}",
        method="POST"
    )

    return Response(twiml.to_xml(), media_type='text/xml')
