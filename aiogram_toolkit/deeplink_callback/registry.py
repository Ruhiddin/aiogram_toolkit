from typing import Callable, Awaitable, Dict, Set, Type, Iterable
from aiogram.filters.callback_data import CallbackData
from .trigger import TriggerSpec

Trigger = Callable[..., Awaitable[bool]]


class CallbackRegistry:
    """
    Central registry mapping (CallbackData class, action) to triggers.

    Frozen after startup.
    """

    def __init__(self) -> None:
        self.cb_classes: Set[Type[CallbackData]] = set()
        self.handlers: Dict[TriggerSpec, Trigger] = {}

    from aiogram.fsm.state import State

    def register(
        self,
        cb_cls: Type[CallbackData],
        action: object | Iterable[object],
        trigger: Trigger,
        *,
        states: Iterable[State | str] | None = None,
    ) -> None:
        self.cb_classes.add(cb_cls)

        actions = action if isinstance(action, (list, tuple, set)) else (action,)

        state_set = (
            frozenset(str(s) for s in states)
            if states is not None
            else None
        )

        for act in actions:
            spec = TriggerSpec(cb_cls, act, state_set)
            if spec in self.handlers:
                raise RuntimeError(
                    f"Duplicate handler for {cb_cls.__name__}.{act} with states={state_set}"
                )
            self.handlers[spec] = trigger


    def resolve(
        self,
        cb: CallbackData,
        current_state: str | None,
    ) -> Trigger | None:

        for spec, trigger in self.handlers.items():
            if spec.cb_cls is not type(cb):
                continue
            if spec.action != cb.action:
                continue

            # no state restriction
            if spec.states is None:
                return trigger

            # state required
            if current_state in spec.states:
                return trigger

        return None
