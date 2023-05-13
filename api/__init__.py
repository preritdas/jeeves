"""
Create the main FastAPI application with routes. Use the `inbound` module main handler. 
Use threading to instantly return a response at the inbound-sms
endpoint.
"""
# External
from fastapi import FastAPI

# Routers
from api import text_inbound, voice_inbound, telegram_inbound
from jeeves.applets.gpt import make_calls


app = FastAPI()


@app.get("/", status_code=200)
def test():
    return f"All working here."


# Include the routers
app.include_router(text_inbound.router, prefix="/texts", tags=["Text Inbound"])
app.include_router(
    telegram_inbound.router, prefix="/telegram", tags=["Telegram Inbound"]
)
app.include_router(voice_inbound.router, prefix="/voice", tags=["Voice Inbound"])
app.include_router(
    make_calls.router, prefix="/voice/outbound", tags=["Voice Outbound Calls"]
)
