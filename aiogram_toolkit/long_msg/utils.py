import re

MDV2_SPECIAL_CHARS = r'\_*[]()~`>#+-=|{}.!'



# ==============______ESCAPE MD V2______=========================================================================================== ESCAPE MD V2
def escape_md_v2(text: str) -> str:
    return re.sub(rf'([{re.escape(MDV2_SPECIAL_CHARS)}])', r'\\\1', text)



# ==============______GET ACTIVE MARKDOWN______=========================================================================================== GET ACTIVE MARKDOWN
def getactive_markdown(text: str) -> list[str]:
    stack = []
    text = re.sub(r'\\.', '', text)

    blocks = re.findall(r'(```|`)', text)
    for token in blocks:
        if stack and stack[-1] == token:
            stack.pop()
        else:
            stack.append(token)

    for symbol in ('*', '_', '~'):
        if text.count(symbol) % 2:
            stack.append(symbol)

    return stack



# ==============______CLOSE OPEN TAGS______=========================================================================================== CLOSE OPEN TAGS
def close_open_tags(text: str, tags: list[str]) -> str:
    return text + ''.join(reversed(tags))



# ==============______REOPEN TAGS______=========================================================================================== REOPEN TAGS
def reopen_tags(tags: list[str]) -> str:
    return ''.join(tags)