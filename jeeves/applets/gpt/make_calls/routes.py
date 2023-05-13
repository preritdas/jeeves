"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response, BackgroundTasks
from twilio.twiml.voice_response import VoiceResponse
from twilio.base.exceptions import TwilioRestException

from urllib.parse import urlencode

from jeeves import voice_tools as vt
from jeeves.texts import twilio_client, BASE_URL

from jeeves.applets.gpt.logs_callback import logger
from jeeves.applets.gpt.make_calls import prompts
from jeeves.applets.gpt.make_calls import database as db


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


def process_user_speech(call_id: str, user_speech: str) -> VoiceResponse:
    """Generate a VoiceResponse based on the user's speech."""
    response = VoiceResponse()

    # Setup the conversation
    current_call = db.Call.from_call_id(call_id)
    current_call.convo += f"\nRecipient: {user_speech}"
    current_call.convo += f"\nJeeves: "

    # Generate response and append to conversation
    ai_response = prompts.generate_response(
        goal=current_call.goal,
        recipient_desc=current_call.recipient_desc,
        convo=current_call.convo
    )
    current_call.convo += ai_response
    logger.info(f"{call_id}: Jeeves: {ai_response}")

    # If Jeeves says its time to hang up
    if "HANGUP" in ai_response or current_call.convo.count("Jeeves:") > 20:
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
    current_call.upload()

    return response


def update_call_with_response(call_id: str, call_sid: str, user_speech: str) -> None:
    """
    Generate a response and update the call with that response.
    """
    response = process_user_speech(call_id=call_id, user_speech=user_speech)

    # Update the call, ignore if the recipient hung up
    try:
        twilio_client.calls(call_sid).update(twiml=response.to_xml())
        logger.info(f"{call_id}: INFO: Call updated with response.")
    except TwilioRestException as e:
        if "Call is not in-progress" in str(e):
            logger.info(f"{call_id}: INFO: Call was ended.")
            return

        raise

    return


@router.post("/handler")
async def handler(call_id: str):
    twiml = VoiceResponse()
    current_call = db.Call.from_call_id(call_id)

    # If no previous conversation is present, start the conversation
    if not current_call.convo:
        logger.info(f"{call_id}: INFO: Handler picked up call.")
        twiml.pause(2)
        twiml.play(current_call.greeting_url)
        current_call.convo = f"Jeeves: {current_call.greeting}"
        current_call.upload()
        logger.info(f"{call_id}: {current_call.convo}")

    # Listen to user response and pass input to /respond
    send_to_respond = {"call_id": call_id}

    twiml.gather(
        action=f"/voice/outbound/respond?{urlencode(send_to_respond)}",
        input="speech",
        speechTimeout=2,
        hints="Jeeves",
        speech_model="experimental_conversations"
    )

    return Response(twiml.to_xml(), media_type="text/xml")


@router.post("/respond")
async def respond(request: Request, call_id: str, background_tasks: BackgroundTasks):
    twiml = VoiceResponse()

    # Grab previous conversations and the user's voice input from the request
    event = await request.form()
    voice_input = event["SpeechResult"]

    background_tasks.add_task(
        update_call_with_response,
        call_id=call_id,
        call_sid=event["CallSid"],
        user_speech=voice_input
    )

    speak(twiml, "One moment, please.")
    twiml.pause(MAX_RESPONSE_TIME)

    logger.info(f"{call_id}: Recipient: {voice_input}")
    logger.info(f"{call_id}: INFO: Pause sent, updater started.")

    return Response(twiml.to_xml(), media_type="text/xml")
