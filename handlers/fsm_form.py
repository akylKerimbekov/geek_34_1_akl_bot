import sqlite3

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, ROOT_PATH
from database.sql_commands import Database


class FormStates(StatesGroup):
    nickname = State()
    bio = State()
    age = State()
    occupation = State()
    photo = State()


async def fsm_start(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Send me your nickname, please"
    )
    await FormStates.nickname.set()


async def load_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["nickname"] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Send me your bio, please"
    )
    await FormStates.next()


async def load_bio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["bio"] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Send me your age, please"
    )
    await FormStates.next()


async def load_age(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["age"] = int(message.text)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Send me your occupation, please"
        )
        await FormStates.next()
    except ValueError as e:
        await message.reply(
            text="failed, because you used not numeric text\n"
                 "please, register again"
        )
        await state.finish()


async def load_occupation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["occupation"] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Send me your photo, please"
    )
    await FormStates.next()


async def load_photo(message: types.Message, state: FSMContext):
    path = await message.photo[-1].download(
        destination_dir=ROOT_PATH + "media"
    )
    async with state.proxy() as data:
        try:
            Database().sql_insert_user_form_query(
                telegram_id=message.from_user.id,
                nickname=data["nickname"],
                bio=data["bio"],
                age=data["age"],
                occupation=data["occupation"],
                photo=path.name,
            )
        except sqlite3.IntegrityError as e:
            await bot.send_message(
                chat_id=message.chat.id,
                text="I have registered"
            )
        with open(path.name, "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"Nickname: {data['nickname']}\n"
                        f"Bip: {data['bio']}\n"
                        f"Age: {data['age']}\n"
                        f"Occupation: {data['occupation']}\n"
            )
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Registered successfully"
        )
        await state.finish()


async def my_profile_call(call: types.CallbackQuery):
    user_form = Database().sql_select_user_form_query(
        telegram_id=call.from_user.id
    )
    try:
        with open(user_form[0]["photo"], "rb") as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=f"Nickname: {user_form[0]['nickname']}\n"
                        f"Bip: {user_form[0]['bio']}\n"
                        f"Age: {user_form[0]['age']}\n"
                        f"Occupation: {user_form[0]['occupation']}\n"
            )
    except IndexError as e:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Try to register your profile first"
        )


def register_fsm_form_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(fsm_start,
                                       lambda call: call.data == "fsm_start")
    dp.register_message_handler(load_nickname,
                                state=FormStates.nickname,
                                content_types=["text"])
    dp.register_message_handler(load_bio,
                                state=FormStates.bio,
                                content_types=["text"])
    dp.register_message_handler(load_age,
                                state=FormStates.age,
                                content_types=["text"])
    dp.register_message_handler(load_occupation,
                                state=FormStates.occupation,
                                content_types=["text"])
    dp.register_message_handler(load_photo,
                                state=FormStates.photo,
                                content_types=types.ContentTypes.PHOTO)
    dp.register_callback_query_handler(my_profile_call,
                                       lambda call: call.data == "my_profile")