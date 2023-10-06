# Standard Library
import asyncio
import functools
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)


def duration(func):
    @contextmanager
    def wrapping_logic():
        start_ts = time.monotonic()
        yield
        dur = time.monotonic() - start_ts
        logging.info(f"{func.__name__} took {dur:2.4f} seconds")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:

            async def tmp():
                with wrapping_logic():
                    return await func(*args, **kwargs)

            return tmp()

    return wrapper
