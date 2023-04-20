# External
from fastapi import APIRouter, Request, Response, BackgroundTasks
from twilio.twiml.voice_response import VoiceResponse
from twilio.base.exceptions import TwilioRestException

# Project
import inbound
import parsing
import texts
import transcribe


router = APIRouter()


RESPONSE_VOICE = "Polly.Arthur-Neural"
MAXIMUM_WAIT_TIME = 180
SPEECH_HINTS = "Jeeves, Google, Todoist, Gmail, Notion, Teams, Discord, Wessential"


def process_speech_update_call(call_sid: str, inbound_phone: str, audio_url: str) -> None:
    """
    Process the speech input from the user. Run it like a text message query.
    The response is spoken to the user and also sent over text.
    """
    # Transcribe the user's speech
    user_speech = transcribe.transcribe_twilio_recording(audio_url)

    response = VoiceResponse()

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
    respond_say = response_content + " " + SUFFIX

    # Parse the content and abide by 1600 character limit
    if len(respond_say) > 1600:
        # If the actual response is also too long
        if len(response_content) > 1600:
            CONCAT_MESSAGE = (
                "That is all I could say over the phone, sir. I have delivered you "
                f"a text message with the full response. {SUFFIX}"
            )
            sendable_content = respond_say[:1600-len(CONCAT_MESSAGE)]
            respond_say = sendable_content + " " + CONCAT_MESSAGE
        # If the response isn't too long but the suffix makes it too long
        # then remove the suffix
        else:
            respond_say = response_content
    
    # Use the <Say> verb to speak the text back to the user
    response.say(respond_say, voice=RESPONSE_VOICE)

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

    # Update the call. This will hang up the call if it is still active.
    # Catching an error raised if the call is not in-progress, as this is okay.
    # All other errors are raised.
    try:
        texts.twilio_client.calls(call_sid).update(twiml=response.to_xml())
    except TwilioRestException as e:
        if "Call is not in-progress" in str(e):
            return
        raise e


@router.api_route("/incoming-call", methods=["GET", "POST"])
async def incoming_call():
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

    # Greet the user
    response.say(
        "Good day, sir, I am at your service. How may I assist you?", 
        voice=RESPONSE_VOICE
    )

    # Collect the user's speech input as a recording for transcription
    response.record(action="/voice/process-speech", timeout=3, play_beep=False)

    # Redirect the call if the user doesn't provide any input
    response.redirect('/voice/incoming-call/')

    return Response(response.to_xml(), media_type='text/xml')


@router.post("/process-speech")
async def process_speech(background_tasks: BackgroundTasks, request: Request):
    """
    
    """
    response = VoiceResponse()
    form = await request.form()

    phone_number = form["From"]
    call_sid = form["CallSid"]
    audio_url = form["RecordingUrl"]

    # Start a background task to process the speech input and generate a response
    background_tasks.add_task(process_speech_update_call, call_sid, phone_number, audio_url)

    # Allow breathing room before ending the call. Updating the call will actually
    # supercede the pause, after testing. So in essence, this is a maximum processing time.
    response.say("On it, sir.", voice=RESPONSE_VOICE)
    response.pause(MAXIMUM_WAIT_TIME)

    # Return blank content to Twilio
    return Response(content=response.to_xml(), media_type='text/xml')
