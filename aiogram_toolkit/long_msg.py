"""
Safe long message splitting for Telegram.

This module provides a break-aware message splitter that allows you to mark
*preferred break points* inside a string using an invisible delimiter.
The delimiter is removed from the final output.

Typical use case:
- Prepare long Telegram messages (>4096 chars)
- Control where messages may be split
- Avoid breaking formatting or semantics

Example:
    text = f"Header{BR}Body{BR}Footer"
    parts = safe_long_msg(text)
"""

from typing import List

#: Default break marker (3× zero-width space)
BR: str = "\u200b" * 3


def set_br(br: str) -> None:
    """
    Set a custom break marker.

    The break marker defines *allowed split points* in text.
    It will be removed from the final output.

    Args:
        br: A string used as a break marker.
    """
    global BR
    BR = br


def safe_long_msg(
    text: str,
    max_len: int = 4096,
) -> List[str]:
    """
    Split a long string into Telegram-safe chunks.

    The function prefers splitting at break markers (`BR`).
    If a single segment exceeds `max_len`, a hard split is applied
    as a fallback.

    Break markers never appear in the output.

    Args:
        text: Input text.
        max_len: Maximum length of each chunk (Telegram limit: 4096).

    Returns:
        A list of message chunks, each <= max_len characters.

    Raises:
        ValueError: If max_len is not positive.
    """
    if max_len <= 0:
        raise ValueError("max_len must be positive")

    if not text:
        return []

    segments = text.split(BR)
    chunks: List[str] = []
    current = ""

    for segment in segments:
        # Hard split if a single segment is too large
        while len(segment) > max_len:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(segment[:max_len])
            segment = segment[max_len:]

        if not current:
            current = segment
        elif len(current) + len(segment) <= max_len:
            current += segment
        else:
            chunks.append(current)
            current = segment

    if current:
        chunks.append(current)

    return chunks
