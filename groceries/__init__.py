from . import classification

def handler(content: str, options: dict):
    # Options
    setup = options.get("setup", None)

    return classification.classify_grocery_list(content, setup=setup)
    