# External
from flask import Flask, request

# Apps
import groceries
import wordhunt


app = Flask(__name__)


PROGRAMS = {
    "groceries": groceries,
    "wordhunt": wordhunt
}


@app.route("/")
def available_apps():
    return "These are the available apps."