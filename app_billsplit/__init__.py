"""Split the bill and vote on tip."""
import utils

from .billsplit_db import test_run


APP_HELP = "Split the bill and vote on the tip."
APP_OPTIONS = {
    "action": "'start' to initiate the split, " \
        "'status' to check on the status, 'end' to make everyone pay.",
    "total": "The total value of the bill, without tip.",
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Handler for the bill split app."""
    return "Hello World"
