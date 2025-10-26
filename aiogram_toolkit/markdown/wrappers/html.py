# HTML wrapper functions for Telegram

def b(string: str) -> str:
    return f"<b>{string}</b>"

def i(string: str) -> str:
    return f"<i>{string}</i>"

def s(string: str) -> str:
    return f"<s>{string}</s>"

def u(string: str) -> str:
    return f"<u>{string}</u>"

def code(string: str) -> str:
    return f"<code>{string}</code>"

def pre(string: str, language: str = "") -> str:
    lang_attr = f' class="language-{language}"' if language else ""
    return f"<pre><code{lang_attr}>{string}</code></pre>"

def link(label: str, url: str) -> str:
    return f'<a href="{url}">{label}</a>'

def mention(label: str, user_id: int) -> str:
    return f'<a href="tg://user?id={user_id}">{label}</a>'

def spoiler(string: str) -> str:
    return f"<span class=\"tg-spoiler\">{string}</span>"
