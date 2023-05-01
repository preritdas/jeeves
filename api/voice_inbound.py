"""Handle incoming calls."""
# External
from fastapi import APIRouter, Request, Response, BackgroundTasks
from twilio.twiml.voice_response import VoiceResponse
from twilio.base.exceptions import TwilioRestException

# Standard library
import re

# Project
import inbound
import parsing
import texts
import voice_tools as vt
from apps.gpt.logs_callback import logger


# Create an API router for voice actions
router = APIRouter()


# Define some constants to be used throughout.
RESPONSE_VOICE = "Polly.Arthur-Neural"  # currently not used, using ElevenLabs
MAXIMUM_WAIT_TIME = 180
SPEECH_HINTS = "Jeeves, Google, Todoist, Gmail, Notion, Teams, Discord, Wessential"  # also inactive


def speak(response: VoiceResponse, text: str) -> None:
    """
    Use the ElevenLabs API to speak the text. Takes in a VoiceResponse object, 
    uses ElevenLabs to speak the text, uses UploadIO to upload the mp3 file and get
    a public-facing audio URL, then adds a <Play> tag to the repsonse object
    containing that public URL.

    Returns nothing because the VoiceResponse object is modified in-place.
    """
    speech_url = vt.speak.speak_jeeves(text)
    response.play(speech_url)


def _process_speech(inbound_phone: str, audio_url: str) -> VoiceResponse:
    """
    Generate a Voice Response object given the user's speech input. Send a follow-up
    text to the user. This method does not catch any errors. It will raise errors 
    as they arise. 
    """
    # Transcribe the user's speech
    user_speech = vt.transcribe.transcribe_twilio_recording(audio_url)

    response = VoiceResponse()

    # Generate raw response content
    if len(user_speech.split()) < 2:
        response_content = "Sir, please call me once more with more to say."
    else:
        inbound_model = parsing.InboundMessage(
            phone_number=inbound_phone,
            body=user_speech
        )
        text_response = inbound.main_handler(
            inbound_sms_content=inbound_model, send_response_message=False
        )
        response_content = text_response["response"]

    # Define what is actually said to the user
    SUFFIX = "That is all, sir. Have a good day."
    respond_say = re.sub(r'\bhttps?:\S+', 'Link here', response_content) + f" {SUFFIX}"
    
    # Use the <Say> verb to speak the text back to the user
    speak(response, respond_say)

    # Hang up the call
    response.hangup()

    # Send the user a text with the response
    texts.send_message(
        content=(
            f"Sir, I helped you over the phone. "
            f"My findings are below for your convenience.\n\n{response_content}"
            f"\n\nAdditionally, sir, the following is what you said to me: {user_speech}"
        ),
        recipient=inbound_phone
    )

    return response


def process_speech_update_call(
    call_sid: str, inbound_phone: str, audio_url: str) -> None:
    """
    Process the speech input from the user. Run it like a text message query.
    The response is spoken to the user and also sent over text. Runs the private
    method to process speech, catching any errors. It then updates the active call
    with the speech, or speaks an error.
    
    We speak errors using the built-in <Say> tag in case errors arise from ElevenLabs
    and/or UploadIO, which are both used to respond in the Jeeves voice.
    """
    try:
        response = _process_speech(
            inbound_phone=inbound_phone, audio_url=audio_url
        )
        logger.info(f"{call_sid} INFO: Successfully processed speech.")
    except Exception as e:
        response = VoiceResponse()
        logger.error(f"{call_sid} ERROR: Failed to process speech. {str(e)}")
        response.say(f"I'm sorry, sir. There was an error. {str(e)}", voice=RESPONSE_VOICE)
    
    # Update the call. This will hang up the call if it is still active.
    # Catching an error raised if the call is not in-progress, as this is okay.
    # All other errors are raised.
    try:
        texts.twilio_client.calls(call_sid).update(twiml=response.to_xml())
        logger.info(f"{call_sid} INFO: Successfully updated call.")
    except TwilioRestException as e:
        if "Call is not in-progress" in str(e):
            logger.info(f"{call_sid} INFO: Call no-longer in-progress.")
            return
        raise e
    

@router.api_route("/incoming-call", methods=["GET", "POST"])
async def incoming_call(request: Request):
    """
    Handle incoming calls. This is the endpoint that Twilio will call when a user
    calls the Twilio number. Routes to the process-speech endpoint which will
    collect the user's speech input and process it.

    This endpoint accepts GET and POST requests. Initially, a POST request is sent
    to initiate the call. Once the call is active, if no input is detected, a GET
    request is sent to this endpoint. Accepting both GET and POST requests allows
    the user to have another chance to speak, as if the call has restarted, without
    having to hang up and call again.
    """
    response = VoiceResponse()
    form = await request.form()

    logger.info(f"{form['CallSid']} INFO: Handler picked up incoming call.")

    # Greet the user
    speak(
        response, 
        "Good day, sir, I am at your service. How may I assist you?", 
    )

    # Collect the user's speech input as a recording for transcription
    response.record(action="/voice/process-speech", timeout=3, play_beep=False)

    return Response(response.to_xml(), media_type='text/xml')


@router.post("/process-speech")
async def process_speech(background_tasks: BackgroundTasks, request: Request):
    """
    This endpoint is triggered after the /inbound-call has handled a call. This endpoint
    will take the user's recording (hosted by Twilio automatically) and route it to a handler
    which will run in a BackgroundTasks instance, handled by FastAPI. It then immediately
    responds with content to avoid a timeout.
    
    It responds with a <Pause> tag. This will hold the call open. Thankfully, once a call
    is updated with speech, the pause tag seems to be abandoned, meaning the user gets a response
    as soon as it is ready. 
    """
    response = VoiceResponse()
    form = await request.form()

    phone_number = form["From"]
    call_sid = form["CallSid"]
    audio_url = form["RecordingUrl"]

    # Start a background task to process the speech input and generate a response
    background_tasks.add_task(
        process_speech_update_call, 
        call_sid, 
        phone_number, 
        audio_url
    )

    # Allow breathing room before ending the call. Updating the call will actually
    # supercede the pause, after testing. So in essence, this is a maximum processing time.
    speak(response, "On it, sir.")
    response.pause(MAXIMUM_WAIT_TIME)

    logger.info(f"{call_sid} INFO: Pause sent, updater task started.")

    # Return blank content to Twilio
    return Response(content=response.to_xml(), media_type='text/xml')
