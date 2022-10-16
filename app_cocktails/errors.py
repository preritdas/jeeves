"""Define the errors and exceptions used in the cocktails app."""

class DrinkNotFoundError(Exception):
    """
    If a drink was searched or requested but couldn't be found in the cocktails database.
    """
    def __init__(self, message: str = ""):
        super().__init__(f"That drink could not be found. {message}")
