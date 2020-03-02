import functools
import loguru

from flask import session, redirect


def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user") is not None:
            return func(*args, **kwargs)
        return redirect("/signin")
    return wrapper
