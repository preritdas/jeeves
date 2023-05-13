"""
Contains all individual apps as submodules, importable with `from apps import billsplit`.
"""
# Local
from typing import Callable

# Apps
from jeeves.applets import groceries
from jeeves.applets import wordhunt
from jeeves.applets import echo
from jeeves.applets import permissions
from jeeves.applets import jokes
from jeeves.applets import weather
from jeeves.applets import invite
from jeeves.applets import usage
from jeeves.applets import rt
from jeeves.applets import cocktails
from jeeves.applets import billsplit
from jeeves.applets import gpt

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
