"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response
from twilio.twiml.voice_response import VoiceResponse

from urllib.parse import urlencode

from . import prompts
from . import database as db


router = APIRouter()


@router.post("/handler")
async def handler(request: Request, call_id: str):
    twiml = VoiceResponse()
  
    # If no previous conversation is present, start the conversation
    convo = db.decode_convo(call_id)
    if not convo:
        intro_message: str = db.decode_greeting(call_id)
        twiml.say(
            intro_message,
            voice="Polly.Joanna-Neural"
        )
        convo = f"AI: {intro_message}"
        db.encode_convo(call_id, convo)

    # Listen to user response and pass input to /respond
    send_to_respond = {"call_id": call_id}
    twiml.gather(
        enhanced=True,
        speech_timeout="auto",
        speech_model="phone_call",
        input="speech",
        action=f"/voice/outbound/respond?{urlencode(send_to_respond)}",
    )

    return Response(twiml.to_xml(), media_type='text/xml')


@router.post("/respond")
async def respond(request: Request, call_id: str):
    twiml = VoiceResponse()

    # Grab previous conversations and the user's voice input from the request
    event = await request.form()
    voice_input = event["SpeechResult"]

    # Format input for GPT-3 and voice the response
    convo = db.decode_convo(call_id)
    goal = db.decode_goal(call_id)

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
    db.encode_convo(call_id, convo)
    send_to_handler = {"call_id": call_id}
    twiml.redirect(
        f"/voice/outbound/handler?{urlencode(send_to_handler)}",
        method="POST"
    )

    return Response(twiml.to_xml(), media_type='text/xml')
