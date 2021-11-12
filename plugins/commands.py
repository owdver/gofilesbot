import os
import re
import ast
import math
import json
import time
import shutil
import asyncio
import pyrogram
import glitchart
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from presets import Presets
  
  
@Client.on_message(filters.private & filters.photo)
async def glitch_art(client, message):
    download_path = PATH + "/" + str(message.from_user.id) + "/"
    download_location = download_path + "photo.jpg"
    message = await message.reply_text(
        text="`Processing...`",
        quote=True
    )
    try:
        await update.download(
            file_name=download_location
        )
    except Exception as error:
        await message.edit_text(
            text=f"**Error :** `{error}`\n\nContact My [Support Group](https://t.me/OB_Links) "
        )
        return 
    await message.edit_text(
        text="`🎨 Converting to glitch...`"
    )
    try:
        glitch_art = glitchart.jpeg(download_location)
        await message.reply_photo(photo=glitch_art, quote=True)
        os.remove(download_location)
        os.remove(glitch_art)
    except Exception as error:
        await message.edit_text(
            text=f"**Error :** `{error}`\n\nContact My [Support Group](https://t.me/OB_Links)"
        )
        return
    await message.delete()


Bot.run()
  
@Client.on_message(filters.command('id') & (filters.private | filters.group))
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"Your ID : `{user_id}`",
            parse_mode="md",
            quote=True
        )
    elif (chat_type == "group") or (chat_type == "supergroup"):
        user_id = message.from_user.id
        chat_id = message.chat.id
        if message.reply_to_message:
            reply_id = f"Replied User ID : `{message.reply_to_message.from_user.id}`"
        else:
            reply_id = ""
        await message.reply_text(
            f"Your ID : `{user_id}`\nThis Group ID : `{chat_id}`\n\n{reply_id}",
            parse_mode="md",
            quote=True
        )
        
@Client.on_message(filters.command('info') & (filters.private | filters.group))
async def showinfo(client, message):
    try:
        cmd, id = message.text.split(" ", 1)
    except:
        id = False
        pass

    if id:
        if (len(id) == 10 or len(id) == 9):
            try:
                checkid = int(id)
            except:
                await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
                return
        else:
            await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
            return           

        if Config.SAVE_USER == "yes":
            name, username, dcid = await find_user(str(id))
        else:
            try:
                user = await client.get_users(int(id))
                name = str(user.first_name + (user.last_name or ""))
                username = user.username
                dcid = user.dc_id
            except:
                name = False
                pass

        if not name:
            await message.reply_text("__USER Details not found!!__", quote=True, parse_mode="md")
            return
    else:
        if message.reply_to_message:
            name = str(message.reply_to_message.from_user.first_name\
                    + (message.reply_to_message.from_user.last_name or ""))
            id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            dcid = message.reply_to_message.from_user.dc_id
        else:
            name = str(message.from_user.first_name\
                    + (message.from_user.last_name or ""))
            id = message.from_user.id
            username = message.from_user.username
            dcid = message.from_user.dc_id
    
    if not str(username) == "None":
        user_name = f"@{username}"
    else:
        user_name = "none"

    await message.reply_text(
        f"<b>Name</b> : {name}\n\n"
        f"<b>User ID</b> : <code>{id}</code>\n\n"
        f"<b>Username</b> : {user_name}\n\n"
        f"<b>Permanant USER link</b> : <a href='tg://user?id={id}'>Click here!</a>\n\n"
        f"<b>DC ID</b> : {dcid}\n\n",
        quote=True,
        parse_mode="html"
    )

        
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘs ➕', url='http://t.me/OB_FILTERROBOT?startgroup=true')
            ],[
            InlineKeyboardButton('🔍 Sᴇᴀʀᴄʜ', switch_inline_query_current_chat=''),
            InlineKeyboardButton('🤖 Uᴘᴅᴀᴛᴇs', url='https://t.me/OB_LINKS')
            ],[
            InlineKeyboardButton('ℹ️ Hᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('😊 Aʙᴏᴜᴛ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.START_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Bot', callback_data='bot'),
            InlineKeyboardButton('Group', callback_data='group')
            ],[
            InlineKeyboardButton('Channel', callback_data='channel'),
            InlineKeyboardButton('Support', url='http://t.me/OwDvEr_BoT')
            ],[
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔐 Cʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "about":
        buttons= [[
            InlineKeyboardButton('🤖 Uᴘᴅᴀᴛᴇs', url='https://t.me/OB_LINKS'),
            InlineKeyboardButton('♥️ Sᴏᴜʀᴄᴇ', callback_data='source')
            ],[
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔐 Cʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.ABOUT_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "group":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.GROUP,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "channel":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.CHANNEL,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "bot":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Format', callback_data='format')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.HOWTO_USE,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "format":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Bᴀᴄᴋ', callback_data='bot')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Presets.FORMAT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
        
