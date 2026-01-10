from aiogram.filters.callback_data import CallbackData
from .config import callback_config

class BaseCB(CallbackData):
    """
    Base class for all typed callback payloads.

    Features:
    - shared CallbackData behavior
    - safe deeplink generation
    """

    def deeplink(self) -> str:
        """
        Generate a /start deeplink with packed payload.

        Example:
            BaseCB(...).deeplink()
        """
        if not callback_config.bot_username:
            raise RuntimeError(
                "callback_config.bot_username is not set. "
                "Call set_bot_username() at startup."
            )

        return (
            f"https://t.me/"
            f"{callback_config.bot_username}"
            f"?start={self.pack()}"
        )