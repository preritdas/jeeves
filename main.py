"""
Create the main Flask application with routes. Use the `inbound` module main handler. 
Use threading to instantly return a response at the inbound-sms
endpoint.
"""
# External
from flask import Flask, request

# Local
import threading

# Project
import inbound
import config


app = Flask(__name__)


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


@app.route("/inbound-sms", methods=["POST"])
def main_handler_wrapper():
    inbound_sms_content = request.get_json()
    print("\n", inbound_sms_content, sep="")

    if type(inbound_sms_content) is not dict:
        return "Not JSON format.", 400

    route_to_handler(inbound_sms_content)
    return "", 204


@app.route("/")
def test():
    return f"All working here.", 200
