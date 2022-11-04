"""
Contains all individual apps as submodules, importable with `from apps import billsplit`.
"""
# Local 
from typing import Callable

# Apps
from . import app_groceries
from . import app_wordhunt
from . import app_echo
from . import app_permissions
from . import app_jokes
from . import app_weather
from . import app_invite
from . import app_usage
from . import app_rt
from . import app_cocktails
from . import app_billsplit

# Project
import utils
import permissions


@utils.app_handler(app_help = "See a list of available apps.")
def handler(content: str, options: dict):
    """Handler for apps. Filters by permissions."""
    accessible_apps: list[str] = [
        f"- {app}" for app in PROGRAMS.keys() if permissions.check_permissions(
            phone = options["inbound_phone"],
            app_name = app
        )
    ]
        
    available_apps = "\n".join(accessible_apps)
    return f"The following apps are available to you - filtered by your permissions.\n\n{available_apps}"


PROGRAMS: dict[str, Callable] = {
    "apps": handler,
    "groceries": app_groceries.handler,
    "wordhunt": app_wordhunt.handler,
    "echo": app_echo.handler,
    "permissions": app_permissions.handler,
    "jokes": app_jokes.handler,
    "weather": app_weather.handler,
    "invite": app_invite.handler,
    "usage": app_usage.handler,
    "rt": app_rt.handler,
    "cocktails": app_cocktails.handler,
    "billsplit": app_billsplit.handler
}
