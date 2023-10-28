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
    Database().sql_insert_result_query(call.message.from_user.id, "yes")
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Yes",
    )


async def no_answer(call: types.CallbackQuery):
    print(call)
    Database().sql_insert_result_query(call.message.from_user.id, "no")
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="No",
    )


async def result_answer(call: types.CallbackQuery):
    print(call)
    rows = Database().sql_select_result_query()
    for row in rows:
        print(f"{row[0]} {row[1]} {row[2]} {row[3]} ")


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire,
                                       lambda call: call.data == "start_questionnaire")
    dp.register_callback_query_handler(yes_answer,
                                       lambda call: call.data == "hungry_yes")
    dp.register_callback_query_handler(no_answer,
                                       lambda call: call.data == "hungry_no")
    dp.register_callback_query_handler(result_answer,
                                       lambda call: call.data == "hungry_result")
