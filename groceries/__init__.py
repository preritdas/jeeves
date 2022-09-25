from . import classification

def handler(content: str):
    # Determine setup
    setup = None
    if "setup" in (first_line := content.splitlines()[0].lower()):
        setup = first_line[7:].title()
        content = "\n".join(content.splitlines()[1:])  # remove setup line

    return classification.classify_grocery_list(content, setup=setup)
    