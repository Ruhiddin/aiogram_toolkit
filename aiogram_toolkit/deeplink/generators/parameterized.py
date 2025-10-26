from .base import BaseGenerator
from aiogram import Bot

class ParameterizedDeeplinkGenerator(BaseGenerator):
    async def generate_deeplink(self, bot: Bot):
        return await self.generate(bot, self.pack())
