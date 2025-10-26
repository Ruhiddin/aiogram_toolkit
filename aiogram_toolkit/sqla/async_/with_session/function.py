from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Callable



def function_with_session(session_factory: Callable[[], AsyncSession], behavior="read"):
    """
    Decorator to manage SQLAlchemy sessions.

    Parameters:
    - behavior: "read" (no commit) or "write" (commit & rollback on failure).
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with session_factory() as session:
                try:
                    kwargs['session'] = session  # Inject session into function
                    result = await func(*args, **kwargs)
                    if behavior == "write":
                        await session.commit()  # Commit only for write operations
                    return result
                except SQLAlchemyError as e:
                    if behavior == "write":
                        await session.rollback()  # Rollback only for write operations
                    raise e
                finally:
                    await session.close()  # Always close session
        return wrapper
    return decorator
