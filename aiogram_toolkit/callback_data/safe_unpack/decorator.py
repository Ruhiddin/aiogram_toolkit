from functools import wraps

def safe_cd_unpack(callback_cls):
    """Decorator to safely unpack callback data for filters."""
    def decorator(filter_func):
        @wraps(filter_func)
        def wrapper(c):
            try:
                cd = callback_cls.unpack(c.data)

                return filter_func(cd)  # Pass unpacked object to the filter function
            except (TypeError, ValueError):
                return False  # Return False if unpacking fails
        return wrapper
    return decorator



def safe_cd_unpack_simple(filter_func):
    """Decorator for methods: safely unpack callback data using self.ctx.cbu.Callback."""
    @wraps(filter_func)
    async def wrapper(self, c):
        try:
            callback_cls = self.ctx.cbu.Callback
            cd = callback_cls.unpack(c.data)
            return await filter_func(self, cd)
        except (AttributeError, TypeError, ValueError):
            return False
    return wrapper
