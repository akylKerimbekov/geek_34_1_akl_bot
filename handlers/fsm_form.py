import random
import re
import sqlite3

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, ROOT_PATH
from database.sql_commands import Database
from keyboard.inline_buttons import like_dislike_keyboard, edit_delete_form_keyboard, my_profile_register_keyboard


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
        user_form = Database().sql_select_user_form_query(
            telegram_id=message.from_user.id
        )
        if user_form:
            Database().sql_update_user_form_query(
                nickname=data["nickname"],
                bio=data["bio"],
                age=data["age"],
                occupation=data["occupation"],
                photo=path.name,
                telegram_id=message.from_user.id,
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
                text="Updated successfully"
            )
        else:
            Database().sql_insert_user_form_query(
                telegram_id=message.from_user.id,
                nickname=data["nickname"],
                bio=data["bio"],
                age=data["age"],
                occupation=data["occupation"],
                photo=path.name,
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
                        f"Occupation: {user_form[0]['occupation']}\n",
                reply_markup=await edit_delete_form_keyboard()
            )
    except IndexError as e:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Try to register your profile first",
            reply_markup=await my_profile_register_keyboard()
        )


async def delete_user_form_call(call: types.CallbackQuery):
    Database().sql_delete_user_form_query(
        owner_telegram_id=call.from_user.id
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Your form was deleted"
    )


async def random_profiles_call(call: types.CallbackQuery):
    user_forms = Database().sql_select_all_user_form_query()
    random_form = random.choice(user_forms)
    with open(random_form["photo"], "rb") as photo:
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=f"Nickname: {random_form['nickname']}\n"
                    f"Bip: {random_form['bio']}\n"
                    f"Age: {random_form['age']}\n"
                    f"Occupation: {random_form['occupation']}\n",
            reply_markup=await like_dislike_keyboard(
                owner_tg_id=random_form["telegram_id"]
            )
        )


async def like_detect_call(call: types.CallbackQuery):
    owner_tg_id = re.sub("user_form_like_", "", call.data)
    try:
        Database().sql_insert_like_query(
            owner_telegram_id=owner_tg_id,
            liker_telegram_id=call.from_user.id
        )
    except sqlite3.IntegrityError as e:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already liked"
        )
    finally:
        await random_profiles_call(call=call)


async def complain_user_call(call: types.CallbackQuery):
    owner_tg_id = re.sub("user_form_complain_", "", call.data)
    try:
        Database().sql_insert_complain_query(
            owner_telegram_id=owner_tg_id,
            complainer_telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=owner_tg_id,
            text="You are in complain list"
        )
    except sqlite3.IntegrityError as e:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already complained"
        )
    finally:
        await random_profiles_call(call=call)


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
    dp.register_callback_query_handler(random_profiles_call,
                                       lambda call: call.data == "random_profile")
    dp.register_callback_query_handler(like_detect_call,
                                       lambda call: "user_form_like_" in call.data)
    dp.register_callback_query_handler(delete_user_form_call,
                                       lambda call: call.data == "delete_user_form")
    dp.register_callback_query_handler(complain_user_call,
                                      lambda call: "user_form_complain_" in call.data)
