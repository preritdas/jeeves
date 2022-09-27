# Personal API

Documentation: [api.preritdas.com](https://api.preritdas.com). 


## Structure Notes

(This is for personal reference.)

Permissions should be a database. Write a `check_permissions` function, called in `app.route("/inbound-sms")`. 


## Style Guide

(This is for personal reference.)

Each app needs a `handler` function callable under the app level, ex. in an app module's `__init__.py`. The handler *must* take exactly two arguments, `content: str` and `options: dict`. Content is the inbound message's raw content. The handler must return string content to be texted back to the user.

Read options with `dict.get` supplying a default option value if the option isn't provided. For example, WordHunt options in the handler...

https://github.com/preritdas/personal-api/blob/a5ff2d2af5b567d0a2dac8b20cddce4a12064f3a/wordhunt/__init__.py#L4-L10

A handler's function signature should be as follows.

```python
def handler(content: str, options: dict) -> str
```


