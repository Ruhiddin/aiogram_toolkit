# MARKDOWN wrapper functions for Telegram (Markdown mode, NOT MarkdownV2)

def b(string: str) -> str:
    return f"*{string}*"

def i(string: str) -> str:
    return f"_{string}_"

def code(string: str) -> str:
    return f"`{string}`"

def pre(string: str) -> str:
    return f"```\n{string}\n```"

def link(label: str, url: str) -> str:
    return f"[{label}]({url})"

def mention(label: str, user_id: int) -> str:
    return f"[{label}](tg://user?id={user_id})"
