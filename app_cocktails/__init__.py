"""Get cocktail drink recommendations with ingredients and instructions."""
import utils

from . import data


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
            return f"No drink was found with the name {content}."

        return data.concat_drinks(drinks, limit=3)

    drink = data.random_cocktail()
    return str(drink)
