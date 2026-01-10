class CallbackConfig:
    """
    Global configuration for callback/deeplink system.
    Must be initialized at startup.
    """
    bot_username: str | None = None


callback_config = CallbackConfig()
