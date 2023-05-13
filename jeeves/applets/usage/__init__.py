"""Read usage data from usage module."""
from jeeves import utils
from jeeves import usage


APP_HELP = "Get a usage report."
APP_OPTIONS = {"date": "Date for usage metrics, ex. 2022-09-27"}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    requested_date = options.get("date")
    return usage.usage_summary(requested_date)
