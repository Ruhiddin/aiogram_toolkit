from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Awaitable, Any

from .registry import CallbackRegistry
from ..logger import logger


class DeeplinkDispatcherMiddleware(BaseMiddleware):
    """
    Middleware that intercepts /start deeplinks and callback queries
    before aiogram routing and dispatches them via CallbackRegistry.
    """

    def __init__(self, registry: CallbackRegistry):
        self.registry = registry

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:

        payload: str | None = None

        # ---- extract payload ---------------------------------------------

        if isinstance(event, Message):
            if not event.text or not event.text.startswith("/start"):
                return await handler(event, data)

            parts = event.text.split(maxsplit=1)
            if len(parts) == 2:
                payload = parts[1]

        elif isinstance(event, CallbackQuery):
            payload = event.data

        if not payload:
            return await handler(event, data)

        # ---- unpack callback ---------------------------------------------

        cb = None
        for cb_cls in self.registry.cb_classes:
            try:
                cb = cb_cls.unpack(payload)
                break
            except Exception:
                continue

        if cb is None:
            return await handler(event, data)

        # ---- resolve trigger ---------------------------------------------
        state: str | None = None
        fsm: FSMContext | None = data.get("state")

        if fsm:
            state = await fsm.get_state()

        trigger = self.registry.resolve(cb, state)
        if not trigger:
            return await handler(event, data)

        # ---- call trigger ------------------------------------------------

        try:
            success = await trigger(event, cb, data)
        except Exception as e:
            # toolkit should log, not crash
            logger.exception("Exception in trigger:\n%s", e)
            return None

        # ---- cleanup -----------------------------------------------------

        if (
            success
            and isinstance(event, Message)
            and event.from_user
            and event.text
            and event.text.startswith("/start")
        ):
            try:
                await event.delete()
            except Exception:
                pass

        return None
