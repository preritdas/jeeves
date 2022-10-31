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


app = Flask(__name__)


@app.route("/inbound-sms", methods=["POST"])
def main_handler_wrapper():
    inbound_sms_content = request.get_json()
    print("\n", inbound_sms_content, sep="")

    if type(inbound_sms_content) is not dict:
        return "Not JSON format.", 400

    process_inbound = threading.Thread(
        target = inbound.main_handler,
        kwargs = {
            "inbound_sms_content": inbound_sms_content
        }
    )
    
    process_inbound.start()  # process the message after returning success
    return "", 204


@app.route("/")
def test():
    return f"All working here.", 200
