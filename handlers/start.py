from aiogram import types, Dispatcher

from config import bot
from database.sql_commands import Database
from keyboard.inline_buttons import (
    start_keyboard,
    admin_keyboard,
)


async def start_button(message: types.Message):
    print(message)
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
