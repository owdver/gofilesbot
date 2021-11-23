# ---------------------------------- https://github.com/m4mallu/gofilesbot ------------------------------------------- #

import re
import os
import time
import random
import asyncio
from bot import Bot
from presets import Presets
from base64 import b64decode
from helper.file_size import get_size
from sample_config import Config
from info import AUTH_CHANNEL, CHANNEL USERNAME
from utils import is_subscribed
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.private & filters.text)
async def bot_pm(client: Bot, message: Message):
    if message.text == "/start":
        buttons = [[
            InlineKeyboardButton('➕ Add Me To Your Group ➕', url=f'http://t.me/OB_FILTERROBOT?startgroup=true')
        ],[
            InlineKeyboardButton('🔍 Search', switch_inline_query_current_chat=''),
            InlineKeyboardButton('🤖 Updates', url='https://t.me/OB_LINKS')
        ],[
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('😊 About', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(Config.PICS),
            caption=Presets.START_TXT.format(message.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.get_chat_invite_link(int(CHANNEL_USERNAME))
        except ChatAdminRequired:
            logger.error("Mᴀᴋᴇ Sᴜʀᴇ Bᴏᴛ Is Aᴅᴍɪɴ Iɴ FᴏʀᴄᴇSᴜʙ Cʜᴀɴɴᴇʟ")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "🤖 Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            btn.append([InlineKeyboardButton(" 🔄 Tʀʏ Aɢᴀɪɴ", callback_data=f"checksub#{message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="*Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Tʜɪs Bᴏᴛ!**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode="markdown"
            )
        return
    if len(message.command) ==2 and message.command[1] in ["subscribe", "error", "okay"]:
        buttons = [[
            InlineKeyboardButton('➕ Add Me To Your Group ➕', url=f'http://t.me/OB_FILTERROBOT?startgroup=true')
        ],[
            InlineKeyboardButton('🔍 Search', switch_inline_query_current_chat=''),
            InlineKeyboardButton('🤖 Updates', url='https://t.me/OB_LINKS')
        ],[
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('😊 About', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(Config.PICS),
            caption=Presets.START_TXT.format(message.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
    try:
        query_message = message.text.split(" ")[-1]
        query_bytes = query_message.encode("ascii")
        base64_bytes = b64decode(query_bytes)
        secret_query = base64_bytes.decode("ascii")
    except Exception:
        msg = await client.send_message(
            chat_id=message.chat.id,
            text=Presets.BOT_PM_TEXT,
            reply_to_message_id=message.message_id
        )
        time.sleep(6)
        try:
            await msg.delete()
            await message.delete()
        except Exception:
            pass
        return
    try:
        await client.send_message(
            chat_id=message.chat.id,
            text=Presets.WELCOME_TEXT.format(message.from_user.first_name),
            parse_mode='html',
            disable_web_page_preview=True
        )
        if secret_query:
            for channel in Config.CHANNELS:
                # Looking for Document type in messages
                async for messages in client.USER.search_messages(channel, secret_query, filter="document", limit=5):
                    doc_file_names = messages.document.file_name
                    if re.compile(rf'{doc_file_names}', re.IGNORECASE):
                        media_name = messages.document.file_name.rsplit('.', 1)[0]
                        await client.send_chat_action(
                            chat_id=message.from_user.id,
                            action="upload_document"
                        )
                        try:
                            await client.copy_message(
                                chat_id=message.chat.id,
                                from_chat_id=messages.chat.id,
                                message_id=messages.message_id,
                                caption=Presets.CAPTION_TEXT_DOC.format(media_name)
                            )
                        except FloodWait as e:
                            time.sleep(e.x)
                # Looking for video type in messages
                async for messages in client.USER.search_messages(channel, secret_query, filter="video", limit=5):
                    vid_file_names = messages.caption
                    if re.compile(rf'{vid_file_names}', re.IGNORECASE):
                        media_name = secret_query.upper()
                        await client.send_chat_action(
                            chat_id=message.from_user.id,
                            action="upload_video"
                        )
                        try:
                            await client.copy_message(
                                chat_id=message.chat.id,
                                from_chat_id=messages.chat.id,
                                message_id=messages.message_id,
                                caption=Presets.CAPTION_TEXT_VID.format(media_name)
                            )
                        except FloodWait as e:
                            time.sleep(e.x)
    except Exception:
        return
