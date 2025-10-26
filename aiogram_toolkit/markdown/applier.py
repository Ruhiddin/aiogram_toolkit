from aiogram.exceptions import TelegramBadRequest
from aiogram.enums.parse_mode import ParseMode


async def try_with_markdown(coroutine, params, force_perform: bool=True, parse_mode: ParseMode=ParseMode.MARKDOWN_V2):
    try:
        return await coroutine(**{'parse_mode': parse_mode}, **params)
    except TelegramBadRequest as e:
        if "can't parse entities" in str(e):
            if force_perform:
                return await coroutine(**params)
        else:
            raise e