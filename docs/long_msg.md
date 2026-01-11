# [← Back to Main Documentation](../README.md)

---

# Safe Long Message Tool

Utility for safely splitting long Telegram messages using **explicit break markers**.

## Overview

Telegram limits messages to **4096 characters**.
This tool allows you to define _preferred break points_ inside a string so splitting happens only where you allow it.

Break markers are **removed** from the final output.

---

## Break Marker

```python
BR = "\u200b" * 3  # default
```

- Invisible (zero-width space)
- Safe for Telegram
- Marks _allowed_ split positions

You may change it globally:

```python
set_br("&&&")
```

---

## API

### `set_br(br: str) -> None`

Set a custom break marker used by `safe_long_msg`.

- Marker is global
- Marker is stripped from output

---

### `safe_long_msg(text: str, max_len: int = 4096) -> List[str]`

Splits text into chunks safe for Telegram.

**Rules:**

- Prefers splitting only at break markers
- Falls back to hard splitting if a single segment is too long
- Output chunks never exceed `max_len`
- Break markers never appear in output

---

## Example

```python
text = f"Header{BR}Body{BR}Footer"
parts = safe_long_msg(text)

# → ["HeaderBodyFooter"] (if fits)
# → ["Header", "BodyFooter"] (if split required)
```

---

## Guarantees

- Deterministic output
- Formatting-safe
- Telegram-ready
- No hidden characters in final messages

---

## Intended Use

- aiogram bots
- Markdown / HTML messages
- Controlled pagination
- Middleware-safe message sending

---

# [← Back to Main Documentation](../README.md)
