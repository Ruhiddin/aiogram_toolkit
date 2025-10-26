from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
from typing import Literal



def with_session(session_factory: Callable[[], AsyncSession], finally_do: Literal['close', 'expunge']='expunge'):
    """
    Decorator to manage SQLAlchemy session lifecycle in an Aiogram handler.

    Args:
        session_factory (callable): A callable that returns a new SQLAlchemy session.

    Returns:
        callable: The decorated handler with a managed session.
    """
    def decorator(handler):
        @wraps(handler)
        async def wrapped_handler(event, *args, **kwargs):
            async with session_factory() as session:
                try:
                    # Pass session explicitly to the handler
                    if kwargs.get('session'):
                        return await handler(event, *args, **kwargs)
                    return await handler(event, session=session, *args, **kwargs)
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    if finally_do == 'expunge':
                        # Do not close or commit the session here; it will be done at the final step
                        session.expunge_all()  # Expunge all objects to avoid keeping unnecessary references
                    else:
                        session.close()

        return wrapped_handler
    return decorator
