from . import classification

def handler(content: str, options: dict):
    # Determine setup
    if "setup" in options: setup = options["setup"]
    else: setup = None

    return classification.classify_grocery_list(content, setup=setup)
    