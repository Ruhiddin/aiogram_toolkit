[← Back to Main Documentation](../README.md)

# Typed Deeplinks & Callback Dispatcher

This module provides a **stateless, typed dispatcher** that unifies:

- `/start <payload>` deeplinks
- inline callback queries

into a **single execution model**, handled **before aiogram routing**.

It is designed for complex bots that require:

- restart safety
- deep navigation via links
- shareable actions
- clean separation between transport and domain logic

---

## Why This Exists

### The Problem With Standard aiogram Flow

In aiogram:

- `/start` is global and hard to customize
- callbacks assume inline buttons only
- deeplinks require ad-hoc parsing
- FSM introduces hidden state and coupling

This breaks down when you need:

- deep navigation (`/start open_folder_42`)
- shareable links
- stateless flows
- domain-level actions

---

### The Solution

This module introduces:

- **typed callback payloads**
- a **central action registry**
- a **dispatcher middleware** that runs _before_ routing

So deeplinks and callbacks become **the same thing**.

---

## Core Concepts

### 1. BaseCB — Typed Payloads

All payloads are defined as subclasses of `BaseCB`.

```python
from aiogram_toolkit.callbacks import BaseCB
from enum import Enum


class NavAction(Enum):
    OPEN_FOLDER = "open"


class NavCB(BaseCB, prefix="nav"):
    action: NavAction
    folder_id: int
```

This payload can be used:

- in inline buttons
- in deeplinks
- in tests

---

### 2. Deeplinks (One-Line)

At startup, configure the bot username **once**:

```python
from aiogram_toolkit.callbacks import set_bot_username

set_bot_username("MyBot")
```

Then generate deeplinks anywhere:

```python
link = NavCB(
    action=NavAction.OPEN_FOLDER,
    folder_id=42,
).deeplink()
```

Result:

```
https://t.me/MyBot?start=nav_open_42
```

No manual encoding.
No string concatenation.

---

### 3. Triggers — Domain Entry Points

Triggers are **pure domain functions**.

```python
async def open_folder_trigger(event, cb: NavCB) -> bool:
    # rebuild UI
    # load folder cb.folder_id
    return True
```

Rules:

- receive unpacked, validated payload
- return `True` to clean up `/start` message
- never delete messages directly
- never parse raw text

---

### 4. Callback Registry — Central Routing

All routing is declared **once at startup**.

```python
from aiogram_toolkit.callbacks import CallbackRegistry

registry = CallbackRegistry()

registry.register(
    cb_cls=NavCB,
    action=NavAction.OPEN_FOLDER,
    trigger=open_folder_trigger,
)
```

Multiple actions can share one trigger:

```python
registry.register(
    cb_cls=FileCB,
    action=[FileAction.RENAME, FileAction.DELETE],
    trigger=file_mutation_trigger,
)
```

This creates a **command bus**, not a router.

---

### 5. Dispatcher Middleware — The Engine

The middleware intercepts:

- `/start <payload>`
- callback queries

before aiogram routing.

```python
from aiogram_toolkit.callbacks import DeeplinkDispatcherMiddleware

dp.update.middleware(
    DeeplinkDispatcherMiddleware(registry)
)
```

What it does:

1. Extract payload
2. Unpack into typed callback
3. Resolve trigger
4. Execute trigger
5. Clean up `/start` message if needed

Your routers remain clean and focused.

---

## Full Minimal Example

```python
# startup.py
from aiogram_toolkit.callbacks import (
    set_bot_username,
    CallbackRegistry,
    DeeplinkDispatcherMiddleware,
)

set_bot_username("MyBot")

registry = CallbackRegistry()
registry.register(NavCB, NavAction.OPEN_FOLDER, open_folder_trigger)

dp.update.middleware(DeeplinkDispatcherMiddleware(registry))
```

That’s all.

---

## When To Use This

Use this system when your bot needs:

- deep navigation
- shareable links
- stateless flows
- restart safety
- domain-driven design
- complex UIs (file managers, dashboards, admin tools)

---

## When _Not_ To Use This

Do **not** use if:

- your bot is command-only
- you rely heavily on FSM
- you don’t need deeplinks
- your flows are trivial

---

## Design Guarantees

- No FSM
- No router coupling
- No string parsing
- Restart-safe
- Fully testable
- Middleware never changes as features grow

---

## Mental Model (Read This Once)

```
Telegram update
 └─ Dispatcher middleware
     ├─ unpack payload
     ├─ resolve action
     ├─ call trigger
     └─ clean up (optional)
```

Everything else is domain logic.

---

## Summary

This module turns callbacks and deeplinks into:

> **typed, stateless commands**

If you build serious Telegram bots, this becomes infrastructure — not a hack.
