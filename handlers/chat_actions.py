from aiogram import types, Dispatcher

from config import bot
from database.sql_commands import Database


async def chat_action(message: types.Message):
    stop_list = ["fuck", "bitch", "damn"]
    print(message.chat.id)
    if message.chat.id == -1002022432879:
        for word in stop_list:
            if word in message.text.lower().replace(" ", ""):
                Database().sql_insert_ban_user_query(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username
                )
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                )
                count = Database().sql_select_ban_user_query(
                    telegram_id=message.from_user.id,
                )
                message_text = f"No curs words in this chat\n"
                f"username: {message.from_user.username}\n"
                f"your behavior is suspicious, and you may be banned"
                if int(count[0]["count"]) >= 3:
                    message_text = f"You will be banned"

                await bot.send_message(
                    chat_id=message.chat.id,
                    text=message_text
                )
    else:
        await message.reply(
            text="There is no such a command\n"
                 "Maybe you mispronounced"
        )


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(chat_action)
