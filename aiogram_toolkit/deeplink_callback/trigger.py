from dataclasses import dataclass
from typing import Type
from aiogram.filters.callback_data import CallbackData

@dataclass(frozen=True)
class TriggerSpec:
    cb_cls: Type[CallbackData]
    action: object
    states: frozenset[str] | None  # None = any state
