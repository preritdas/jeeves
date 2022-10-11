"""Rotten Tomatoes app."""
import rottentomatoes as rt

import utils


APP_HELP = "Rotten tomatoes info on movies. Specify the movie title as message content."


@utils.app_handler(APP_HELP)
def handler(content: str, options: dict) -> str:
    """Handler for the Rotten Tomatoes app."""
    if not content:
        return "You didn't specify a movie."
    
    try:
        movie = rt.Movie(content)
    except rt.LookupError:
        return f"'{content}' wasn't found on Rotten Tomatoes."

    return str(movie)
