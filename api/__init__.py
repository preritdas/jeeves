"""
Create the main FastAPI application with routes. Use the `inbound` module main handler. 
Use threading to instantly return a response at the inbound-sms
endpoint.
"""
# External
from fastapi import FastAPI, Request

# Routers
from api import text_inbound, voice_inbound, telegram_inbound, voice_outbound, authentication


app = FastAPI(
    title="Jeeves Backend API",
    description="Full backend powering Jeeves. Note that ALL routes are protected."
)


@app.get("/", status_code=200)
def test(request: Request):
    return {
        "json": request.json(),
        "path_params": dict(request.path_params),
        "query_params": (request.query_params)
    }


# Include the routers
app.include_router(text_inbound.router, prefix="/texts", tags=["Text Inbound"])
app.include_router(
    telegram_inbound.router, prefix="/telegram", tags=["Telegram Inbound"]
)
app.include_router(voice_inbound.router, prefix="/voice", tags=["Voice Inbound"])
app.include_router(
    voice_outbound.router, prefix="/voice/outbound", tags=["Voice Outbound Calls"]
)
app.include_router(authentication.router, prefix="/auth", tags=["Authentication"])
