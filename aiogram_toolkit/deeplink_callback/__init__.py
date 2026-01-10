from .config import callback_config
from .base import BaseCB
from .registry import CallbackRegistry
from .middleware import DeeplinkDispatcherMiddleware

__all__ = [
    "BaseCB",
    "CallbackRegistry",
    "DeeplinkDispatcherMiddleware",
]




def set_bot_username(username: str) -> None:
    """
    Set bot username for deeplink generation.

    Must be called once at application startup.
    """
    callback_config.bot_username = username
