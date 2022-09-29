"""Utilities for everything."""

def app_handler(app_help: str, app_options: dict = {}):
    """
    Handler decorator that automatically returns help options if requested in 
    the handler's required `options` parameter.
    """
    app_help += "\n\n"

    def wrapper_func(function):
        def inner(content: str, options: dict[str, str]):
            if not "help" in options:
                return function(content, options)

            if not app_options:
                return app_help + "There are no available options."
            
            option_messages = []
            for option, message in app_options.items():
                option_messages.append(f"- {option.lower()}: {message.lower()}")
            
            return app_help + "Available options:\n" + "\n".join(option_messages)
        
        return inner

    return wrapper_func
