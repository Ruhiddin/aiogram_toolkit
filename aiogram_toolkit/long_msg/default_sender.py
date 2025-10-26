import re
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram_toolkit.long_msg.utils import close_open_tags, escape_md_v2, getactive_markdown, reopen_tags
from aiogram_toolkit.markdown.applier import try_with_markdown
from aiogram_toolkit.shortcuts import P_NOPREV
from aiogram_toolkit.sqla_dashboard.memory.memory_cluster import MemoryCluster



async def send_long_message(
    bot: Bot,
    chat_id: int,
    text: str,
    message_id: int | None = None,
    markdown: bool = False,
    first_edit: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
    message_thread_id: int = None,
    
    dialog_memory: MemoryCluster = None
) -> int | None:
    """
    Sends or edits a long message in multiple chunks.

    ### Args:
        `bot` (Bot): The bot instance.
        `chat_id` (int): The ID of the chat to send/edit messages.
        `text` (str): The full message text.
        `message_id` (int, optional): Original message ID (used if replying or editing).
        `markdown` (bool): Enable MarkdownV2 formatting.
        `first_edit` (bool): Edit first chunk instead of sending.
        `reply_markup` (InlineKeyboardMarkup, optional): Inline keyboard.
        `edit_by_id` (int, optional): Message ID to edit directly.

        `memory` (MemoryCluster) - Memory Cluster instance

    ### Returns:
        `int | None`: ID of the last sent message if `is_dialog` else None.
    """
    max_len = 4096
    sent_message_ids: list[int] = []
    active_tags: list[str] = []
    buffer = ''
    first_chunk_done = False

    lines = text.splitlines(keepends=True)

    for line in lines:
        test_chunk = buffer + line
        if markdown:
            test_chunk = escape_md_v2(test_chunk)

        if len(test_chunk) > max_len:
            chunk = close_open_tags(buffer, active_tags) if markdown else buffer
            params = {
                "chat_id": chat_id,
                "text": chunk,
                "reply_markup": reply_markup,
                **P_NOPREV
            }

            if first_edit and not first_chunk_done and message_id:
                params['message_id'] = message_id
                method = bot.edit_message_text
                first_chunk_done = True
            else:
                params["message_thread_id"] = message_thread_id

                method = bot.send_message

            sent_msg = await try_with_markdown(method, params) if markdown else await method(**params)
            if sent_msg:
                sent_message_ids.append(sent_msg.message_id)

            if markdown:
                active_tags = getactive_markdown(buffer)
                buffer = reopen_tags(active_tags) + line
            else:
                buffer = line
        else:
            buffer = test_chunk if not markdown else re.sub(r'\\(.)', r'\1', test_chunk)

    if buffer.strip():
        final_chunk = close_open_tags(buffer, active_tags) if markdown else buffer
        params = {
            "chat_id": chat_id,
            "text": final_chunk,
            "reply_markup": reply_markup,
            **P_NOPREV
        }

        if first_edit and not first_chunk_done and message_id:
            params['message_id'] = message_id
            method = bot.edit_message_text
        else:
            params["message_thread_id"] = message_thread_id

            method = bot.send_message

        sent_msg = await try_with_markdown(method, params) if markdown else await method(**params)
        if sent_msg:
            sent_message_ids.append(sent_msg.message_id)

    last_message_id = None
    if dialog_memory is not None and sent_message_ids:
        last_message_id = sent_message_ids.pop()
        await dialog_memory.trash_long_msg_ids.set(sent_message_ids)
        await dialog_memory.dialog_msg_id.set(last_message_id)

    return last_message_id
