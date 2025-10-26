from functools import wraps
from typing import Callable, Literal


def with_session(
    session_factory: Callable[[], "AsyncSession"], # type: ignore  # noqa: F821
    finally_do: Literal["close", "expunge"] = "expunge"
):
    """
    Decorator to manage SQLAlchemy session lifecycle in an Aiogram handler.

    Args:
        session_factory (callable): A callable returning a new SQLAlchemy AsyncSession.
        finally_do (str): 'close' or 'expunge' — defines final session handling.
    """
    def decorator(handler):
        @wraps(handler)
        async def wrapped_handler(event, *args, **kwargs):
            # Lazy import to avoid loading SQLAlchemy globally
            from sqlalchemy.ext.asyncio import AsyncSession

            async with session_factory() as session:
                try:
                    if "session" in kwargs:
                        return await handler(event, *args, **kwargs)
                    return await handler(event, session=session, *args, **kwargs)
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    if finally_do == "expunge":
                        session.expunge_all()
                    else:
                        # AsyncSession.close() is a coroutine
                        close_method = getattr(session, "close", None)
                        if close_method and callable(close_method):
                            maybe_coro = close_method()
                            if maybe_coro is not None:
                                await maybe_coro

        return wrapped_handler
    return decorator
