import binascii
import os

from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import _create_link

from config import bot
from database.sql_commands import Database
from keyboard.inline_buttons import reference_menu_keyboard


async def reference_menu_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"Hello {call.from_user.first_name}\n"
             f"glad to see you in reference menu",
        reply_markup=await reference_menu_keyboard()
    )


async def reference_link_call(call: types.CallbackQuery):
    user = Database().sql_select_user_query(
        telegram_id=call.from_user.id
    )
    if not user[0]["link"]:
        token = binascii.hexlify(os.urandom(8)).decode()
        link = await _create_link(link_type="start", payload=token)
        Database().sql_update_user_ref_query(
            reference_link=link,
            telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Hello {call.from_user.first_name}\n"
                 f"here your link {link}"
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Hello {call.from_user.first_name}\n"
                 f"here your link from db {user[0]['link']}",
            reply_markup=await reference_menu_keyboard()
        )


async def reference_list_call(call: types.CallbackQuery):
    referrals = Database().sql_select_all_referral_by_owner_query(
        owner_telegram_id=call.from_user.id
    )
    if referrals:
        data = [f"[{user['referral_telegram_id']}](tg://user?id={user['referral_telegram_id']})" for user in referrals]
        await bot.send_message(
            chat_id=call.from_user.id,
            text="\n".join(data),
            parse_mode=types.ParseMode.MARKDOWN
        )


async def wallet_balance_call(call: types.CallbackQuery):
    balance = Database().sql_select_wallet_balance_by_owner_query(
        owner_telegram_id=call.from_user.id
    )

    if balance:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Your balance: {balance[0]['balance']}",
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Invite someone to top up your wallet",
        )


def register_reference_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(reference_menu_call,
                                       lambda call: call.data == "reference_menu")
    dp.register_callback_query_handler(reference_link_call,
                                       lambda call: call.data == "reference_link")
    dp.register_callback_query_handler(reference_list_call,
                                       lambda call: call.data == "reference_list")
    dp.register_callback_query_handler(wallet_balance_call,
                                       lambda call: call.data == "wallet_balance")
