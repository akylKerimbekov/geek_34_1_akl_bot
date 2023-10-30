import re
import sqlite3

from aiogram import types, Dispatcher

from config import bot
from database.sql_commands import Database
from keyboard.inline_buttons import news_menu_keyboard
from scraper.news_scraper import NewsScraper


async def news_list_menu_call(call: types.CallbackQuery):
    scraper = NewsScraper()
    news = scraper.parse_data(call.from_user.id)

    for item in news:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=item.title,
            reply_markup=await news_menu_keyboard(
                news_id=item.id
            )
        )


async def update_news_detect_call(call: types.CallbackQuery):
    news_id = re.sub("update_news_link_", "", call.data)
    try:
        Database().sql_update_fav_news_query(
            news_id=news_id
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Saved as favorite"
        )
    except sqlite3.IntegrityError as e:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already saved as favorite"
        )


async def fav_news_list_menu_call(call: types.CallbackQuery):
    fav_news = Database().sql_select_all_fav_news_query(
        owner_telegram_id=call.from_user.id
    )
    if fav_news:
        for news in fav_news:
            await bot.send_message(
                chat_id=call.from_user.id,
                text=news["title"],
            )


def register_news_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(news_list_menu_call,
                                       lambda call: call.data == "news_list_menu")
    dp.register_callback_query_handler(update_news_detect_call,
                                       lambda call: "update_news_link_" in call.data)
    dp.register_callback_query_handler(fav_news_list_menu_call,
                                       lambda call: call.data == "fav_news_list_menu")
