from aiogram.utils.deep_linking import create_start_link

class BaseGenerator:
    async def generate(bot, param_str):
        link = await create_start_link(bot, param_str, encode=True)
        return link