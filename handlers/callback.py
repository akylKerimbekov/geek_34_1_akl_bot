from aiogram import types, Dispatcher
from database.sql_commands import Database
from config import bot
from keyboard.inline_buttons import questionnaire_one_keyboard


async def start_questionnaire(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Are you hungry?",
        reply_markup=await questionnaire_one_keyboard()
    )


async def yes_answer(call: types.CallbackQuery):
    print(call)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Yes",
    )


async def no_answer(call: types.CallbackQuery):
    print(call)
    await bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="No",
    )


async def admin_user_list_call(call: types.CallbackQuery):
    users = Database().sql_select_all_user_query()
    ids = [user["username"] for user in users]
    await bot.send_message(
        chat_id=call.from_user.id,
        text="\n".join(ids)
    )


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire,
                                       lambda call: call.data == "start_questionnaire")
    dp.register_callback_query_handler(yes_answer,
                                       lambda call: call.data == "hungry_yes")
    dp.register_callback_query_handler(no_answer,
                                       lambda call: call.data == "hungry_no")
    dp.register_callback_query_handler(admin_user_list_call,
                                       lambda call: call.data == "admin_user_list")
