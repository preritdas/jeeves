![pytest](https://github.com/preritdas/personal-api/actions/workflows/pytest.yml/badge.svg)
![coverage](tests/badge.svg)
![docs](https://github.com/preritdas/personal-api/actions/workflows/docs.yml/badge.svg)
![gcp](https://github.com/preritdas/personal-api/actions/workflows/google-cloud.yml/badge.svg)


# Personal API

Documentation: [api.preritdas.com](https://api.preritdas.com). 


## Structure Notes

(This is for personal reference.)

All done


## Style Guide

(This is for personal reference.)

Each app needs a `handler` function callable under the app level, ex. in an app module's `__init__.py`. The handler *must* take exactly two arguments, `content: str` and `options: dict`. Content is the inbound message's raw content. The handler must return string content to be texted back to the user. The main handler always passes an `inbound_phone` key in the `options` dictionary to each app.

```python
# Default options payload
options: dict[str, str] = {
    "inbound_phone": "12223334455"
}
```

Read options with `dict.get` supplying a default option value if the option isn't provided. For example, WordHunt options in the handler...

https://github.com/preritdas/personal-api/blob/a5ff2d2af5b567d0a2dac8b20cddce4a12064f3a/wordhunt/__init__.py#L4-L10

A handler's function signature should be as follows.

```python
def handler(content: str, options: dict) -> str
```


