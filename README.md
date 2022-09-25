# Personal API


## Structure Notes

(This is for personal reference.)

Permissions should be a database. Write a `check_permissions` function, called in `app.route("/inbound-sms")`. 


## Style Guide

(This is for personal reference.)

Each app needs a `handler` function callable under the app level, ex. in an app module's `__init__.py`. The handler *must* take exactly two arguments, `content: str` and `user: str`. In that order. Content is the inbound message's raw content. User is the phone number.