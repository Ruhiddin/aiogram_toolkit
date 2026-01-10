from typing import Callable, Awaitable, Dict, Set, Tuple, Type, Iterable
from aiogram.filters.callback_data import CallbackData

Trigger = Callable[..., Awaitable[bool]]


class CallbackRegistry:
    """
    Central registry mapping (CallbackData class, action) to triggers.

    Frozen after startup.
    """

    def __init__(self) -> None:
        self.cb_classes: Set[Type[CallbackData]] = set()
        self.handlers: Dict[Tuple[Type[CallbackData], object], Trigger] = {}

    def register(
        self,
        cb_cls: Type[CallbackData],
        action: object | Iterable[object],
        trigger: Trigger,
    ) -> None:
        """
        Register a trigger for one or multiple actions.

        Raises:
            RuntimeError on duplicate registrations.
        """
        self.cb_classes.add(cb_cls)

        actions = action if isinstance(action, (list, tuple, set)) else (action,)

        for act in actions:
            key = (cb_cls, act)
            if key in self.handlers:
                raise RuntimeError(
                    f"Duplicate handler for {cb_cls.__name__}.{act}"
                )
            self.handlers[key] = trigger

    def resolve(self, cb: CallbackData) -> Trigger | None:
        """
        Resolve trigger for unpacked callback payload.
        """
        return self.handlers.get((type(cb), cb.action))
