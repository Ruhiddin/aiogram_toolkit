from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from typing import List, Dict




async def get_paginated_page(
        page_data: List[Dict[str, str | InlineKeyboardButton]], 
        page: int, 
        table_count: int,
        current_count: int, 
        total_list_pages: int, 
        btns_per_row: int = 6, 
        list_name: str = 'Unknown Data',
        control_btns: List[InlineKeyboardButton] = [],
        extra_btns_top: List[List[InlineKeyboardButton]] = [[]], 
        extra_btns_bottom: List[List[InlineKeyboardButton]] = [[]]
    ):
    """
    Generates a paginated page message with inline buttons based on current page data.
    
    Args:
        page_data: list - data of the current page to be displayed in the menu.
            [
                {
                    'string': "", 
                    'button': InlineKeyboardButton()
                },
                ...
            ]
        prefix: str - callback prefix for the control buttons.
        page: int - current page number.
        current_count: int - total number of items in the list.
        total_list_pages: int - total number of pages in list.
        btns_per_row: int - number of buttons per row (default: 8).
        items_per_page: int - number of items per page (default: 20).
        list_name: str - name of the list (default: 'Data').
        extra_btns_top: list - list of extra buttons to be displayed at the top (default: [[]]).
        extra_btns_bottom: list - list of extra buttons to be displayed at the bottom (default: [[]]).
    
    Returns:
        tuple: A message text and an inline keyboard for the current page.
    """
    page_items_count = len(page_data)

    title = f"📜{page_items_count} ✨{current_count} 📦{table_count}  📂{list_name} 👁‍🗨: {page}/{total_list_pages}"

    header= f'{title}\n\n'[:40]
    footer = f'\n\n{title}'[:40]
    message_text = (
        f"{header}"
        f'{"\n".join(item["string"] for item in page_data)}'
        f"{footer}"   
    )

    markup = InlineKeyboardBuilder()

    # Top extra buttons
    for extra_btn in extra_btns_top:
        markup.row(*extra_btn)
    
    # Item buttons
    has_btns = page_data and page_data[0].get('button')
    if has_btns:
        buttons = [item['button'] for item in page_data]
        for i in range(0, len(buttons), btns_per_row):
            markup.row(*buttons[i:i + btns_per_row])

    # Control buttons
    prev_btn, next_btn = control_btns[0], control_btns[1]

    if page > 1 and page < total_list_pages:
        markup.row(
            prev_btn,
            next_btn
        )
    elif page > 1:
        markup.row(prev_btn)
    elif page < total_list_pages:
        markup.row(next_btn)
        
    # Bottom extra buttons
    for extra_btn in extra_btns_bottom:
        markup.row(*extra_btn)
    
    return message_text, markup.as_markup()