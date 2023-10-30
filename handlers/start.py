import sqlite3

from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import _create_link

from config import bot
from database.sql_commands import Database
from keyboard.inline_buttons import (
    start_keyboard,
    admin_keyboard,
)


async def start_button(message: types.Message):
    print(message)
    print(message.get_full_command())
    command = message.get_full_command()
    if command[1] != "":
        link = await _create_link(link_type="start", payload=command[1])
        owner = Database().sql_select_user_by_link_query(
            link=link
        )
        if owner[0]["telegram_id"] == message.from_user.id:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You can not use own referral link"
            )
            return

        try:
            Database().sql_insert_referral_query(
                owner_telegram_id=owner[0]["telegram_id"],
                referral_telegram_id=message.from_user.id
            )
        except sqlite3.IntegrityError as e:
            pass



    Database().sql_insert_user_query(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    with open("/Users/Akylbek_Kerimbekov/PycharmProjects/geek_34_1_akl_bot/media/bot_pic.png", "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"Hello {message.from_user.first_name} I am your first bot",
            reply_markup=await start_keyboard()
        )


async def secret_word(message: types.Message):
    if message.from_user.id == 5107969242:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Long time no see, master {message.from_user.first_name}",
            reply_markup=await admin_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="No permission"
        )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(secret_word, lambda word: "dorei" in word.text)
