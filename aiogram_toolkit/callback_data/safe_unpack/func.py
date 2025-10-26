from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData


def safe_cd_unpack(c: CallbackQuery, callback_cls: CallbackData):
    try:
        return callback_cls.unpack(c.data)
    except (TypeError, ValueError):
        return False