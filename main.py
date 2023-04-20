"""
Create the main FastAPI application with routes. Use the `inbound` module main handler. 
Use threading to instantly return a response at the inbound-sms
endpoint.
"""
# External
from fastapi import FastAPI, Form, Request, Response
from twilio.twiml.voice_response import VoiceResponse

# Local
import threading

# Project
import inbound
import config
import parsing
import texts


app = FastAPI()

RESPONSE_VOICE = "Polly.Brian-Neural"


def route_to_handler(inbound_sms_content: parsing.InboundMessage) -> None:
    """
    Routes inbound sms content to the main handler, and reads the config's
    stated preference of threaded responses to either handle the inbound in a thread
    (simply start the thread) or to wait for the processing to complete.
    """
    if config.General.THREADED_INBOUND:
        process_inbound = threading.Thread(
            target = inbound.main_handler,
            kwargs = {
                "inbound_sms_content": inbound_sms_content
            }
        )
        process_inbound.start()
    else:
        inbound.main_handler(inbound_sms_content=inbound_sms_content)


@app.post("/inbound-sms", status_code=204)
def main_handler_wrapper(From: str = Form(...), Body: str = Form(...)):
    """Handle the inbound, routing it to the handler."""
    # Validate the data
    inbound_model = parsing.InboundMessage(phone_number=From, body=Body)

    # Process the request
    route_to_handler(inbound_model)

    return ""


@app.api_route("/incoming-call", methods=['GET', 'POST'])
async def incoming_call():
    """
    Handle incoming calls. This is the endpoint that Twilio will call when a user
    calls the Twilio number. Routes to the process-speech endpoint which will
    collect the user's speech input and process it.
    """
    response = VoiceResponse()

    # Use Twilio's <Gather> verb to collect user's speech input
    gather = response.gather(
        input='speech',
        action='/process-speech/',  # The endpoint to process the speech input
        timeout=5,
        hints='yes, no',  # Optional: provide hints for better speech recognition
        language='en-US'
    )
    gather.say('Good day, sir, at your service. How may I assist you?', voice=RESPONSE_VOICE)

    # Redirect the call if the user doesn't provide any input
    response.redirect('/incoming-call/')

    return Response(response.to_xml(), media_type='text/xml')


@app.api_route("/process-speech/", methods=['GET', 'POST'])
async def process_speech(request: Request):
    """
    Process the speech input from the user. Run it like a text message query.
    The response is spoken to the user and also sent over text.
    """
    twilio_request = await request.form()
    inbound_phone_number = twilio_request.get('From', '')

    user_speech = twilio_request.get('SpeechResult', '').strip()
    response = VoiceResponse()

    if user_speech:
        inbound_model = parsing.InboundMessage(
            phone_number=inbound_phone_number,
            body=user_speech
        )
        text_response = inbound.main_handler(
            inbound_sms_content=inbound_model, send_response_message=False
        )["response"]
        
        # Use the <Say> verb to speak the text back to the user
        response.say(text_response, voice=RESPONSE_VOICE)

        # Send the user a text with the response
        texts.send_message(
            content=(
                f"Sir, I helped you over the phone. "
                f"My findings are below for your convenience.\n\n{text_response}"
            ),
            recipient=twilio_request.get('From', '')
        )

    else:
        # If no speech input was detected, inform the user
        response.say("Sorry, I didn't catch that. Please try again.")

    # Redirect user back to incoming-call so they can say something else
    response.redirect('/incoming-call/')

    return Response(response.to_xml(), media_type='text/xml')


@app.get("/", status_code=200)
def test():
    return f"All working here."
