# Overview


```{note}
All inbound sms app requests are made automatically by Nexmo to the `/inbound-sms` endpoint.
```


When a text message is sent to the receiver number, Nexmo sends a `POST` request to the server containing the text content, sender information, and any relevant metadata. A typical message takes the following format.

```text
app: groceries
options: setup = whole foods; add = true; id = 87asdf6

2 bananas
3 apples
ice cream
```

## Validation

As long as this message is under 160 characters, it's accepted and handled internally. If it's more than 160 characters or otherwise fails basic validation, an error text message is sent back.

1. Firstly, the message is checked for a required app name. Content/options are no longer required---it's possible to use an app simply by calling the app's name (ex. the [apps](apps.md) applet).

```{literalinclude} ../../../parsing.py
:pyobject: assert_valid
```

2. Then, the server ensures the inbound message is not part of a series of concatenated messages. If a text message is sent with more than 160 characters, Nexmo chops it up and pings the server once for each concatenated block.

```{literalinclude} ../../../parsing.py
:pyobject: is_concat
```

The server is run using `gunicorn` with several workers. With only one worker, it's entirely possible to handle concatenated messages as one large text block by caching/storing inbound messages. With multiple workers, however, each works independently. The server is designed such that each worker can handle an inbound text message from start to finish.

3. The requested app is then checked for existence. All applets are registered within the [apps](apps) app.

```{literalinclude} ../../../apps/__init__.py
```


## Structure

As is visible in the above [apps](apps.md) source, each applet needs a `handler` function, including the [apps](apps.md) applet itself. The handler must be callable at the app's root level, ex. `apps.handler` if `apps` is imported.

The handler *must* take exactly two arguments, `content: str` and `options: dict`. `content` is the inbound message's raw text content, post validation. `options` comes from parsing (section below). The handler must return string content to be texted back to the user.

A handler's function signature should be as follows.

```python
def handler(content: str, options: dict) -> str
```

Because options are (obviously) optional, they should be read with the `dict.get` method, supplying a default value if the option isn't provided. For example, the WordHunt handler is below.

```{literalinclude} ../../../wordhunt/__init__.py
:pyobject: handler
```


## Parsing

Once a text message is received and has passed basic validation, some simple functions are used to determine the requested app and to parse the given options. 

```{literalinclude} ../../../parsing.py
:pyobject: requested_app
```

Parsing the options is slightly more tricky. Options are given in the following format.

```text
options: something = yes; something_else = no
```

This has to be turned into a dictionary.

```python
{
    "something": "yes",
    "something_else": "no"
}
```

Currently all option values are interpreted as strings. No conversions are made to numeric or boolean types. Any type-specific checking must (currently) happen at the applet level. So, within an app, the following lines will check if an optional boolean was set as true.

```python
if options.get("do_something", None):
    ...
```

In this way, if `"do_something"` is not a key in `options: dict` (i.e. it was not given by the user), the `dict.get` function returns `None`, evaluated as `False`, which prevents the ensuing conditional. The downside is that if a user provides `do_something = false` in their `options: ` line, `do_something` will be evaluated as `True`, as it is passed to the handler as `{"do_something": "false"}`---a non-empty string literal.

Options are parsed by splitting the line containing `"options:"`, if it exists. If not, an empty dictionary `{}` is returned and passed to the handler.

```{literalinclude} ../../../parsing.py
:pyobject: _parse_options
```

The above `_parse_options` function is called internally by `app_content_options`, which is the public function called by `main.main_handler`---the entrypoint for all inbound sms messages.

```{literalinclude} ../../../parsing.py
:pyobject: app_content_options
```
