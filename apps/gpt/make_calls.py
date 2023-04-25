"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from twilio.twiml.voice_response import VoiceResponse
import deta

from texts import twilio_client
from keys import KEYS


router = APIRouter()
convo_base = deta.Deta(KEYS["Deta"]["project_key"]).Base("conversations")


def generate_response():
    return "This is a response."





def encode_convo(convo: str) -> str:
    """Stores and returns ID."""
    res = convo_base.put({"convo": convo})
    print(f"Encoded: {res['key']}")
    return res["key"]


def decode_convo(convo_id: str):
    """Uses ID to find convo."""
    res = convo_base.get(convo_id)["convo"]
    print(f"Decoded: {res}")
    return res


@router.post("/handler")
async def handler(request: Request, convo: str = None):
    twiml = VoiceResponse()

    if convo:
        convo = decode_convo(convo)
  
    # If no previous conversation is present, start the conversation
    if not convo:
        twiml.say(
            "Hey!",
            voice="Polly.Joanna-Neural"
        )
        convo = "Joanna: Hey!"

    # Listen to user response and pass input to /respond
    twiml.gather(
        enhanced=True,
        speech_timeout="auto",
        speech_model="phone_call",
        input="speech",
        action=f"/voice/outbound/respond?convo={encode_convo(convo)}",
    )

    return Response(twiml.to_xml(), media_type='text/xml')


@router.post("/respond")
async def respond(request: Request, convo: str = None):
    twiml = VoiceResponse()

    # Grab previous conversations and the user's voice input from the request
    event = await request.form()
    voice_input = event["SpeechResult"]

    # Format input for GPT-3 and voice the response
    convo = decode_convo(convo)
    convo += f"\nYou: {voice_input}\nJoanna: "
    ai_response = f"You said {voice_input}, sir."
    convo += ai_response
    twiml.say(
        ai_response,
        voice="Polly.Joanna-Neural"
    )

    # Pass new convo back to /listen
    twiml.redirect(
        f"/voice/outbound/handler?convo={encode_convo(convo)}",
        method="POST"
    )

    return Response(twiml.to_xml(), media_type='text/xml')
