"""
MARKDOWN_V2 wrapper functions for Telegram
(b | i | s | u | code | pre | link | mention | spoiler | escape_string)
Reference: https://core.telegram.org/bots/api#markdownv2-style
"""

def b(string: str, escape: bool = False) -> str:
    """Wraps string with BOLD entity."""
    return f"*{escape_string(string) if escape else string}*"

def i(string: str, escape: bool = False) -> str:
    """Wraps string with ITALIC entity."""
    return f"_{escape_string(string) if escape else string}_"

def s(string: str, escape: bool = False) -> str:
    """Wraps string with STRIKETHROUGH entity."""
    return f"~{escape_string(string) if escape else string}~"

def u(string: str, escape: bool = False) -> str:
    """Wraps string with UNDERLINE entity."""
    return f"__{escape_string(string) if escape else string}__"

def code(string: str, escape: bool = True) -> str:
    """Wraps string with INLINE CODE entity."""
    return f"`{escape_string(string) if escape else string}`"

def pre(string: str, language: str = "", escape: bool = False) -> str:
    """
    Wraps string with CODE BLOCK entity.
    Optionally specify a programming language.
    """
    content = escape_string(string) if escape else string
    return f"```{language}\n{content}\n```"

def link(label: str, url: str, escape: bool = True) -> str:
    """
    Creates a link with specified label and URL.
    Example: [label](https://example.com)
    """
    escaped_label = escape_string(label) if escape else label
    escaped_url = escape_string(url, for_link=True) if escape else url
    return f"[{escaped_label}]({escaped_url})"

def mention(label: str, user_id: int, escape: bool = False) -> str:
    """
    Creates a mention with specified label and user ID.
    Example: [label](tg://user?id=123456789)
    """
    escaped_label = escape_string(label) if escape else label
    return f"[{escaped_label}](tg://user?id={user_id})"

def spoiler(string: str, escape: bool = False) -> str:
    """Wraps string with SPOILER entity."""
    return f"||{escape_string(string) if escape else string}||"

def escape_string(string: str='', for_link: bool = False) -> str:
    """
    Escapes special characters for Markdown V2 formatting.
    If `for_link` is True, parentheses are escaped as well.
    """
    special_chars = r"_*[]()~`>#+-=|{}.!"
    if for_link:
        special_chars += "()"
    return "".join(f"\\{char}" if char in special_chars else char for char in string)
