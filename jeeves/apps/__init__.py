"""
Contains all individual apps as submodules, importable with `from apps import billsplit`.
"""
# Local
from typing import Callable

# Apps
from jeeves.apps import groceries
from jeeves.apps import wordhunt
from jeeves.apps import echo
from jeeves.apps import permissions
from jeeves.apps import jokes
from jeeves.apps import weather
from jeeves.apps import invite
from jeeves.apps import usage
from jeeves.apps import rt
from jeeves.apps import cocktails
from jeeves.apps import billsplit
from jeeves.apps import gpt

# Project
from jeeves import utils
from jeeves import permissions as perms


@utils.app_handler(app_help="See a list of available apps.")
def handler(content: str, options: dict):
    """Handler for apps. Filters by permissions."""
    accessible_apps: list[str] = [
        f"- {app}"
        for app in PROGRAMS.keys()
        if perms.check_permissions(phone=options["inbound_phone"], app_name=app)
    ]

    available_apps = "\n".join(accessible_apps)
    return f"The following apps are available to you - filtered by your permissions.\n\n{available_apps}"


PROGRAMS: dict[str, Callable] = {
    "apps": handler,
    "groceries": groceries.handler,
    "wordhunt": wordhunt.handler,
    "echo": echo.handler,
    "permissions": permissions.handler,
    "jokes": jokes.handler,
    "weather": weather.handler,
    "invite": invite.handler,
    "usage": usage.handler,
    "rt": rt.handler,
    "cocktails": cocktails.handler,
    "billsplit": billsplit.handler,
    "gpt": gpt.handler
}
