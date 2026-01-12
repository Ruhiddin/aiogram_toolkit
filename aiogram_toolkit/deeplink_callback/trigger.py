from dataclasses import dataclass
from typing import Type
from aiogram.filters.callback_data import CallbackData
from typing import Protocol
from aiogram.types import TelegramObject


class Trigger(Protocol):
    async def __call__(
        self,
        event: TelegramObject,
        cb: CallbackData,
        data: dict,
    ) -> bool: ...



@dataclass(frozen=True)
class TriggerSpec:
    cb_cls: Type[CallbackData]
    action: object
    states: frozenset[str] | None  # None = any state
