"""Get cocktail drink recommendations with ingredients and instructions."""
import utils
import config

from . import data
from . import errors  # unit tests


APP_HELP = (
    "Get cocktail drink recommendations with ingredients and instructions. "
    "You can search for a drink by providing it as content. "
    "The top three results are sent back."
)
APP_OPTIONS = {}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    """Gather and report the drink info. String format it."""
    if content:  # searching for a drink
        drinks = data.search_cocktails(content)

        if not drinks:
            return f"I didn't find any drinks with the query '{content}'."

        return data.concat_drinks(drinks, limit=config.Cocktails.RESULT_LIMIT)

    drink = data.random_cocktail()
    return str(drink)
