import asyncio
from functools import wraps


def async_task(f):
    """Adapter for sync task to make them async."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
