"""Make outbound calls with an outcome or goal in mind."""
from fastapi import APIRouter, Request, Response
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from twilio.twiml.voice_response import VoiceResponse
import deta

from urllib.parse import urlencode

from texts import twilio_client
from keys import KEYS


router = APIRouter()
convo_base = deta.Deta(KEYS["Deta"]["project_key"]).Base("conversations")
llm = ChatOpenAI(openai_api_key=KEYS["OpenAI"]["api_key"], model_name="gpt-4")


PREFIX_MESSAGE = (
    "You are a conversational AI. You receive a conversation "
    "between you and a recipient (whom you called) and complete it with your "
    "response, and ONLY YOUR OWN RESPONSE. DO NOT make up recipient responses. "
    "\n\nYour job is to facilitate a GOAL. Once you determine the GOAL "
    "has been achieved, you can end the conversation by responding with HANGUP. "
    "\n\n---------- Example: \n\n"
    "GOAL: Order a pizza to 1 Main Street, New York, NY.\n\nConversation:\n\n"
    "Recipient: Hello?\nAI: Hi, I'd like to order a pizza to 1 Main Street.\n"
    "Recipient: What kind of pizza?\nAI: Pepperoni.\nRecipient: What size?\n"
    "AI: Large.\nRecipient: What's your name?\nAI: John.\nRecipient: We'll "
    "get that to you in 30 minutes, John.\nAI: Thanks, bye.\nRecipient: Bye.\n"
    "AI: HANGUP\n\n----------\n\n"
    "GOAL: {goal}\n\nComplete the conversation below with only one response "
    "from you, the AI.\n\n{conversation}"
)

prompt_template = PromptTemplate(
    input_variables=["goal", "conversation"],
    template=PREFIX_MESSAGE,
)

conversation_chain = LLMChain(
    prompt=prompt_template,
    llm=llm
)


def generate_response(convo: str) -> str:
    return conversation_chain.run(goal="Have a pleasant conversation.", conversation=convo)


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
  
    # # If no previous conversation is present, start the conversation
    # if not convo:
    #     twiml.say(
    #         "Hey!",
    #         voice="Polly.Joanna-Neural"
    #     )
    #     convo = "AI: Hey, what's up?"

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
    ai_response = generate_response(convo)
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
