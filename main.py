# External
from flask import Flask, request

# Apps
import apps


app = Flask(__name__)


@app.route("/inbound-sms")
def main_handler():
    """
    Handle all inbound messages.
    
    Keep this as simple as possible, with plenty of outsourcing.
    """
    inbound_sms_content = request.get_json()
    print("\n", inbound_sms_content, sep="")

    if type(inbound_sms_content) is not dict:
        return '', 400




if __name__ == '__main__':
    apps.handler("a", "a")