"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response
from twilio.twiml.voice_response import VoiceResponse

from urllib.parse import urlencode

from . import prompts
from . import database as db
import voice_tools as vt


router = APIRouter()


def speak(response: VoiceResponse, text: str) -> None:
    """
    Use the ElevenLabs API to speak the text. Takes in a VoiceResponse object, 
    uses ElevenLabs to speak the text, uses UploadIO to upload the mp3 file and get
    a public-facing audio URL, then adds a <Play> tag to the repsonse object
    containing that public URL.
    """
    speech_url = vt.speak.speak_jeeves(text)
    response.play(speech_url)


@router.post("/handler")
async def handler(request: Request, call_id: str):
    twiml = VoiceResponse()
  
    # If no previous conversation is present, start the conversation
    convo = db.decode_convo(call_id)
    if not convo:
        intro_message: str = db.decode_greeting(call_id)
        speak(twiml, intro_message)
        convo = f"Jeeves: {intro_message}"
        db.encode_convo(call_id, convo)

    # Listen to user response and pass input to /respond
    send_to_respond = {"call_id": call_id}

    # Record the recipient talking
    twiml.record(
        action=f"/voice/outbound/respond?{urlencode(send_to_respond)}",
        timeout=3,
        play_beep=False
    )

    return Response(twiml.to_xml(), media_type='text/xml')


@router.post("/respond")
async def respond(request: Request, call_id: str):
    twiml = VoiceResponse()

    # Grab previous conversations and the user's voice input from the request
    event = await request.form()
    recording_url = event['RecordingUrl']

    # Format input for GPT-3 and voice the response
    convo = db.decode_convo(call_id)
    goal = db.decode_goal(call_id)

    # Transcribe the input
    voice_input = vt.transcribe.transcribe_twilio_recording(recording_url)

    convo += f"\nRecipient: {voice_input}\nJeeves: "
    ai_response = prompts.generate_response(goal, convo)
    convo += ai_response
    speak(twiml, ai_response)

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
