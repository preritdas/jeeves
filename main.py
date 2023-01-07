"""
Create the main FastAPI application with routes. Use the `inbound` module main handler. 
Use threading to instantly return a response at the inbound-sms
endpoint.
"""
# External
from fastapi import FastAPI

# Local
import threading

# Project
import inbound
import config
import parsing


app = FastAPI()


def route_to_handler(inbound_sms_content: dict) -> None:
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
def main_handler_wrapper(inbound: parsing.NexmoInbound):
    """Handle the inbound, routing it to the handler."""
    print("\n", inbound, sep="")
    print(inbound.dict())
    route_to_handler(inbound.dict())

    return ""


@app.get("/", status_code=200)
def test():
    return f"All working here."
