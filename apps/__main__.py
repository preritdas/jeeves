"""Directly interact with applets. For testing purposes only."""
import sys
import json

from . import PROGRAMS


if len(sys.argv) < 2:
    print("You must provide an app name.")
    sys.exit()

APP_NAME: str = sys.argv[1]

if len(sys.argv) > 2:
    CONTENT = sys.argv[2]
else:
    CONTENT = ""

if len(sys.argv) > 3:
    OPTIONS = json.loads(sys.argv[3])
else:
    OPTIONS = {}

OPTIONS["inbound_phone"] = "00000000000"


if not APP_NAME in PROGRAMS:
    print(f"App {APP_NAME} not found.")
    sys.exit()


# Get response
response = PROGRAMS[APP_NAME](
    content = CONTENT,
    options = OPTIONS
)


print(response)
