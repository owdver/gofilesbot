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

imdb = IMDb() 

BANNED = {}
SMART_OPEN = '“'
SMART_CLOSE = '”'
START_CHAR = ('\'', '"', SMART_OPEN)

# temp db for banned 
class temp(object):
    BANNED_USERS = []
    BANNED_CHATS = []
    ME = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

async def is_subscribed(bot, query):
    try:
        user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception as e:
        logger.exception(e)
    else:
        if user.status != 'kicked':
            return True

    return False

    imdb = await get_poster(search, file=(files[0]).file_name) if IMDB else None
    if imdb:
        cap = IMDB_TEMPLATE.format(
            query = search,
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url']
        )
    else:
        cap = f"Here is what i found for your query {search}"
    if imdb and imdb.get('poster'):
        try:
            await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await message.reply_photo(photo=poster, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    if spoll:
        await msg.message.delete()

async def auto_filter(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:
         
        search = message.text
        files, offset, total_results = await get_search_results(search.lower(), offset=0)
        if not files:
            return
        if SINGLE_BUTTON:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                    ),
                ]
                for file in files
            ]
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}",
                        callback_data=f'files#{file.file_id}',
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}",
                        callback_data=f'files_#{file.file_id}',
                    ),
                ]
                for file in files
            ]

        if offset != "":
            key = f"{message.chat.id}-{message.message_id}"
            BUTTONS[key] = search
            req = message.from_user.id if message.from_user else 0
            btn.append(
                [InlineKeyboardButton(text=f"🗓 1/{round(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_{req}_{key}_{offset}")]
            )
        else:
            btn.append(
                [InlineKeyboardButton(text="🗓 1/1",callback_data="pages")]
            )
        imdb=await get_poster(search)
        if imdb and imdb.get('poster'):
            await message.reply_photo(photo=imdb.get('poster'), caption=f"<b>Qᴜᴇʀʏ: {search}</b> \n‌‌‌‌Iᴍᴅʙ Dᴀᴛᴀ:\n\n🏷 Tɪᴛʟᴇ: <a href={imdb['url']}>{imdb.get('title')}</a>\n🎭 Gᴇɴʀᴇs: {imdb.get('genres')}\n📆 Yᴇᴀʀ: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n🌟 Rᴀᴛɪɴɢ: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10", reply_markup=InlineKeyboardMarkup(btn))
        elif imdb:
            await message.reply_text(f"<b>Qᴜᴇʀʏ: {search}</b> \n‌‌‌‌Iᴍᴅʙ Dᴀᴛᴀ:\n\n🏷 Tɪᴛʟᴇ: <a href={imdb['url']}>{imdb.get('title')}</a>\n🎭 Gᴇɴʀᴇs: {imdb.get('genres')}\n📆 Yᴇᴀʀ: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n🌟 Rᴀᴛɪɴɢ: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10", reply_markup=InlineKeyboardMarkup(btn))
        else:
            await message.reply_text(f"<b>Hᴇʀᴇ Is Wʜᴀᴛ I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ {search} ‌‌‌‌‎ </b>", reply_markup=InlineKeyboardMarkup(btn))
    
    
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
                async for messages in client.USER.search_messages(channel, query_message, filter="document", limit=50):
                    doc_file_names = messages.document.file_name
                    file_size = get_size(messages.document.file_size)
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
                                text=Presets.ASK_PM_TEXT,
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
                        media_format = messages.document.file_name.split('.')[-1]
                        try:
                            await client.copy_message(
                                chat_id=message.from_user.id,
                                from_chat_id=messages.chat.id,
                                message_id=messages.message_id,
                                caption=Config.GROUP_U_NAME+Presets.CAPTION_TEXT_DOC.format(media_name,
                                                                                            media_format, file_size)
                            )
                        except FloodWait as e:
                            time.sleep(e.x)
                        user_message[id] = message.message_id
                # Looking for video type in messages
                async for messages in client.USER.search_messages(channel, query_message, filter="video", limit=50):
                    vid_file_names = messages.caption
                    file_size = get_size(messages.video.file_size)
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
                            await client.send_message(
                                chat_id=message.chat.id,
                                message.reply_photo(photo=imdb.get('poster'),
                                text=Presets.ASK_PM_TEXT,
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
                                caption=Config.GROUP_U_NAME+Presets.CAPTION_TEXT_VID.format(media_name, file_size)
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
                    text=Presets.MEDIA_SEND_TEXT,
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
                    text=Presets.NO_MEDIA.format(query_message, updated_query),
                    reply_to_message_id=message.message_id,
                    parse_mode='html',
                    disable_web_page_preview=True
                )
            except Exception:
                pass
