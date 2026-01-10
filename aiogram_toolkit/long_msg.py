from typing import List

ZERO_WIDTH = "\u200b"
DEFAULT_SPLIT_POINT = ZERO_WIDTH * 3


def safe_long_msg(
    text: str,
    max_len: int = 4096,
    split_point: str = DEFAULT_SPLIT_POINT,
) -> List[str]:
    if max_len <= 0:
        raise ValueError("max_len must be positive")

    parts = text.split(split_point)
    chunks: List[str] = []
    current = ""

    for part in parts:
        if not current:
            current = part
        elif len(current) + len(part) <= max_len:
            current += part
        else:
            chunks.append(current)
            current = part

        # brutal fallback: still too big, hard split
        while len(current) > max_len:
            chunks.append(current[:max_len])
            current = current[max_len:]

    if current:
        chunks.append(current)

    return chunks
