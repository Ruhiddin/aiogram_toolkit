from typing import List

BR = "\u200b" * 3

def set_br(br: str = "\u200b" * 3) -> None:
    global BR 
    BR = br

def safe_long_msg(
    text: str,
    max_len: int = 4096,
) -> List[str]:
    if max_len <= 0:
        raise ValueError("max_len must be positive")

    if not text:
        return []

    segments = text.split(BR)
    chunks: List[str] = []
    current: str = ""

    for segment in segments:
        # If segment itself is too large → hard split
        while len(segment) > max_len:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(segment[:max_len])
            segment = segment[max_len:]

        # Try to append segment to current chunk
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
