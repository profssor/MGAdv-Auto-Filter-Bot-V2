#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserNotParticipant
from bot import Translation # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error

db = Database()

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    update_channel = "@MG_MEDIA"
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked out":
               await update.reply_text("๐คญ Sorry Dude, You are B A N N E D ๐คฃ๐คฃ๐คฃ")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="๐๐จ๐ฎ ๐ฆ๐ฎ๐ฌ๐ญ ๐ฃ๐จ๐ข๐ง ๐จ๐ฎ๐ซ ๐๐ก๐๐ง๐ง๐๐ฅ ๐จ๐ญ๐ก๐๐ซ๐ฐ๐ข๐ฌ๐ ๐๐ก๐ข๐ฌ ๐๐จ๐๐ญ ๐ข๐ฌ ๐ฎ๐ง๐ฎ๐ฌ๐๐๐ฅ๐\n<b>๊ฑสแดสแด แดษดแด ๊ฑแดแดแดแดสแด\n\n<a href='https://t.me/MG_MEDIA'>ยฉ๊ฐษชสแด แดขแดษดแด</a></b>",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text=" ๐ฐJOIN OUR CHANNEL๐ฐ ", url=f"https://t.me/MG_MEDIA")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return   
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        
        if file_type == "document":
        
            await bot.send_document(
                chat_id=update.chat.id,
                document = file_id,
                caption = caption,
                parse_mode="html",
                reply_to_message_id=update.message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'โ?๏ธJOIN CHANNELโ?๏ธ', url="https://t.me/joinchat/nppwyzxMr8NhN2M9"
                                )
                        ]
                    ]
                )
            )

        elif file_type == "video":
        
            await bot.send_video(
                chat_id=update.chat.id,
                video = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'โ?๏ธJOIN CHANNELโ?๏ธ', url="https://t.me/joinchat/nppwyzxMr8NhN2M9"
                                )
                        ]
                    ]
                )
            )
            
        elif file_type == "audio":
        
            await bot.send_audio(
                chat_id=update.chat.id,
                audio = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'โ?๏ธJOIN CHANNELโ?๏ธ', url="https://t.me/joinchat/nppwyzxMr8NhN2M9"
                                )
                        ]
                    ]
                )
            )

        else:
            print(file_type)
        
        return

    buttons = [[
        InlineKeyboardButton('๐ฃCHANNEL', url='https://t.me/joinchat/nppwyzxMr8NhN2M9'),
        InlineKeyboardButton('GROUP๐ฌ', url ='http://t.me/MGmoviegram')
    ],[
        InlineKeyboardButton('OWNERโจ', url='https://t.me/Wafikh')
    ],[
        InlineKeyboardButton('Help โ', callback_data="help")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(
                update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home โก', callback_data='start'),
        InlineKeyboardButton('About ๐ฉ', callback_data='about')
    ],[
        InlineKeyboardButton('Close ๐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Home โก', callback_data='start'),
        InlineKeyboardButton('Close ๐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )
