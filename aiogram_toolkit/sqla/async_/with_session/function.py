from functools import wraps
from typing import Callable


def function_with_session(session_factory: Callable[[], "AsyncSession"], behavior="read"): # type: ignore  # noqa: F821
    """
    Decorator to manage SQLAlchemy sessions, with lazy imports.

    Parameters:
    - behavior: "read" (no commit) or "write" (commit & rollback on failure).
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Lazy import to avoid loading SQLAlchemy until needed
            from sqlalchemy.ext.asyncio import AsyncSession
            from sqlalchemy.exc import SQLAlchemyError

            async with session_factory() as session:
                try:
                    kwargs["session"] = session
                    result = await func(*args, **kwargs)
                    if behavior == "write":
                        await session.commit()
                    return result
                except SQLAlchemyError:
                    if behavior == "write":
                        await session.rollback()
                    raise
                finally:
                    await session.close()

        return wrapper

    return decorator
