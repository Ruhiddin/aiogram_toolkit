

# ==============______ MARKDOWN______===========================================================================================  MARKDOWN
async def escape_md(text):
    """
    Escape all standard Markdown-specific characters so they are treated as regular text.
    
    Args:
        text (str): The input text to be escaped.
    
    Returns:
        str: The escaped text.
    """
    escape_chars = r'\_*[]()#<>`+-|{}.!'
    escaped_text = ''.join(f'\\{char}' if char in escape_chars else char for char in text)
    return escaped_text



# ==============______MARKDOWN V2______=========================================================================================== MARKDOWN V2
def escape_md_v2(text):
    """
    Escape all Markdown V2-specific characters so they are treated as regular text.
    
    Args:
        text (str): The input text to be escaped.
    
    Returns:
        str: The escaped text.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    # Escape Markdown V2 restricted characters
    text = str(text)
    escaped_text = ''.join(f'\\{char}' if char in escape_chars else char for char in text)
    return escaped_text


# ==============______ HTML______===========================================================================================  HTML
async def escape_html(text):
    """
    Escape special HTML characters so they are treated as regular text.
    
    Args:
        text (str): The input text to be escaped.
    
    Returns:
        str: The escaped text.
    """
    # Replace common HTML special characters with their entity equivalents
    html_escape_mapping = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    escaped_text = ''.join(html_escape_mapping.get(char, char) for char in text)
    return escaped_text
