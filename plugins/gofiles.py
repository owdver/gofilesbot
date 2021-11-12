# ----------------------------------- https://github.com/m4mallu/gofilesbot ------------------------------------------ #

import re
import os
import time
import asyncio

from bot import Bot
from presets import Presets
from base64 import b64encode
from init import user_message
from helper.file_size import get_size
from imdb import IMDb
from pyrogram import Client, filters
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

if os.environ.get("ENV", False):
    from sample_config import Config
else:
    from config import Config
    
@Client.on_message(filters.group & filters.text)
async def query_mgs(client: Bot, message: Message):
    query_message = message.text
    block_list = Presets.BLOCK_LIST
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if query_message.startswith(tuple(block_list)):
        return
    info = await client.get_me()
    user_message.clear()
    if len(message.text) > 2:
        try:
            for channel in Config.CHANNELS:
                # Looking for Document type in messages
                async for messages in client.USER.search_messages(channel, query_message, filter="document", limit=10):
                    doc_file_names = messages.document.file_name
                    if re.compile(rf'{doc_file_names}', re.IGNORECASE):
                        try:
                            await client.send_chat_action(
                                chat_id=message.from_user.id,
                                action="upload_document"
                            )
                        except Exception:
                            query_bytes = query_message.encode("ascii")
                            base64_bytes = b64encode(query_bytes)
                            secret_query = base64_bytes.decode("ascii")
                            await client.send_message(
                                chat_id=message.chat.id,
                                text=Presets.ASK_PM_TEXT.format(query_message),
                                reply_to_message_id=message.message_id,
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [InlineKeyboardButton(
                                            "👉 CLICK HERE 👈", url="t.me/{}?start={}".format(info.username, secret_query))
                                         ]
                                    ])
                            )
                            return
                        media_name = messages.document.file_name.rsplit('.', 1)[0]
                        try:
                            await client.copy_message(
                                chat_id=message.from_user.id,
                                from_chat_id=messages.chat.id,
                                message_id=messages.message_id,
                                caption=Presets.CAPTION_TEXT_DOC.format(media_name)
                            )
                        except FloodWait as e:
                            time.sleep(e.x)
                        user_message[id] = message.message_id
                # Looking for video type in messages
                async for messages in client.USER.search_messages(channel, query_message, filter="video", limit=10):
                    vid_file_names = messages.caption
                    if re.compile(rf'{vid_file_names}', re.IGNORECASE):
                        try:
                            await client.send_chat_action(
                                chat_id=message.from_user.id,
                                action="upload_video"
                            )
                        except Exception:
                            query_bytes = query_message.encode("ascii")
                            base64_bytes = b64encode(query_bytes)
                            secret_query = base64_bytes.decode("ascii")
                            await client.send_photo(
                                chat_id=message.chat.id,
                                caption=Presets.ASK_PM_TEXT.format(query_message),
                                reply_to_message_id=message.message_id,
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [InlineKeyboardButton(
                                            "👉 CLICK HERE 👈", url="t.me/{}?start={}".format(info.username, secret_query))
                                         ]
                                    ])
                            )
                            return
                        media_name = message.text.upper()
                        try:
                            await client.copy_message(
                                chat_id=message.from_user.id,
                                from_chat_id=messages.chat.id,
                                message_id=messages.message_id,
                                caption=Presets.CAPTION_TEXT_VID.format(media_name)
                            )
                        except FloodWait as e:
                            time.sleep(e.x)
                        user_message[id] = message.message_id
        except Exception:
            try:
                await client.send_message(
                    chat_id=message.chat.id,
                    text=Presets.PM_ERROR,
                    reply_to_message_id=message.message_id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                "👉 START BOT 👈", url="t.me/{}".format(info.username))
                             ]
                        ])
                )
            except Exception:
                pass
            return
        if user_message.keys():
            try:
                await client.send_message(
                    chat_id=message.chat.id,
                    text=Presets.MEDIA_SEND_TEXT.format(query_message),
                    reply_to_message_id=user_message[id],
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                "👉 Click Here To View 👈", url="t.me/{}".format(info.username))
                             ]
                        ])
                )
                user_message.clear()
            except Exception:
                pass
        else:
            updated_query = query_message.replace(" ", "+")
            try:
                await client.send_message(
                    chat_id=message.chat.id,
                    text=Presets.NO_MEDIA.format(query_message, query_message),
                    reply_to_message_id=message.message_id,
                    parse_mode='html',
                    disable_web_page_preview=True,
                    buttons = [[
                        InlineKeyboardButton('Mᴜsᴛ Rᴇᴀᴅ | Cʟɪᴄᴋ Hᴇʀᴇ', url='http://t.me/OB_FILTERROBOT?startgroup=true')
                    ],[
                        InlineKeyboardButton('Gᴏᴏɢʟᴇ Sᴇᴀʀᴄʜ', url="https://www.google.com/search?q={}".format(updated_query))
                    ]]
                )
            except Exception:
                pass
