import functools
import loguru

from flask import session, redirect

logger = loguru.logger


def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(session.get("user"))
        if session.get("user") is not None:
            return func(*args, **kwargs)
        return redirect('/signin')
    return wrapper
