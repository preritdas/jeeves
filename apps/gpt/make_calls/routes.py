"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response, BackgroundTasks
from twilio.twiml.voice_response import VoiceResponse
from twilio.base.exceptions import TwilioRestException

from urllib.parse import urlencode

import voice_tools as vt
from texts import twilio_client, BASE_URL

from . import prompts
from . import database as db


router = APIRouter()


# Maximum seconds to respond to each input from user
MAX_RESPONSE_TIME: int = 45


def speak(response: VoiceResponse, text: str) -> None:
    """
    Use the ElevenLabs API to speak the text. Takes in a VoiceResponse object, 
    uses ElevenLabs to speak the text, uses UploadIO to upload the mp3 file and get
    a public-facing audio URL, then adds a <Play> tag to the repsonse object
    containing that public URL.
    """
    speech_url = vt.speak.speak_jeeves(text)
    response.play(speech_url)


def update_call_with_response(call_id: str, call_sid: str, user_speech: str) -> None:
    """
    Generate a response and update the call with that response.
    """
    response = VoiceResponse()

    # Setup the conversation
    convo = db.decode_convo(call_id)
    convo += f"\nRecipient: {user_speech}"
    convo += f"\nJeeves: "

    # Generate response and append to conversation
    ai_response = prompts.generate_response(
        goal=db.decode_goal(call_id), 
        recipient_desc=db.decode_recipient_desc(call_id),
        convo=convo
    )
    convo += ai_response

    # If Jeeves says its time to hang up
    if "HANGUP" in ai_response or convo.count("Jeeves:") > 20:
        speak(response, "Thanks for speaking with me. Goodbye.")
        response.hangup()
    else:  # continue the conversation
        speak(response, ai_response)

        # Send the response to the handler for more user input
        send_to_handler = {"call_id": call_id}
        response.redirect(
            f"{BASE_URL}/voice/outbound/handler?{urlencode(send_to_handler)}",
            method="POST"
        )

    # Update the conversation record
    db.encode_convo(call_id, convo)

    # Update the call, ignore if the recipient hung up
    try:
        twilio_client.calls(call_sid).update(twiml=response.to_xml()) 
    except TwilioRestException as e:
        if "Call is not in-progress" in str(e):
            return
         
        raise
    
    return


@router.post("/handler")
async def handler(request: Request, call_id: str):
    twiml = VoiceResponse()
  
    # If no previous conversation is present, start the conversation
    convo = db.decode_convo(call_id)
    if not convo:
        twiml.pause(2)
        twiml.play(db.decode_greeting_url(call_id))
        convo = f"Jeeves: {db.decode_greeting(call_id)}"
        db.encode_convo(call_id, convo)

    # Listen to user response and pass input to /respond
    send_to_respond = {"call_id": call_id}

    twiml.gather(
        action=f"/voice/outbound/respond?{urlencode(send_to_respond)}",
        input="speech",
        speechTimeout=3,
        hints="Jeeves",
        speech_model="experimental_conversations"
    )

    return Response(twiml.to_xml(), media_type='text/xml')


@router.post("/respond")
async def respond(request: Request, call_id: str, background_tasks: BackgroundTasks):
    twiml = VoiceResponse()

    # Grab previous conversations and the user's voice input from the request
    event = await request.form()
    voice_input = event['SpeechResult']

    background_tasks.add_task(
        update_call_with_response,
        call_id=call_id,
        call_sid=event['CallSid'],
        user_speech=voice_input
    )

    speak(twiml, "One moment, please.")
    twiml.pause(MAX_RESPONSE_TIME)

    return Response(twiml.to_xml(), media_type='text/xml')
