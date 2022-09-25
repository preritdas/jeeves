# Personal API


## Structure Notes

(This is for personal reference.)

Permissions should be a database. Write a `check_permissions` function, called in `app.route("/inbound-sms")`. 


## Style Guide

(This is for personal reference.)

Each app needs a `handler` function callable under the app level, ex. in an app module's `__init__.py`. The handler *must* take exactly two arguments, `content: str` and `options: dict`. Content is the inbound message's raw content. The handler must return string content to be texted back to the user.
