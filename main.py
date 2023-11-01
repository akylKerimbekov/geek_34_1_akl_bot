import asyncio

from aiogram import executor

from config import dp
from database.sql_commands import Database
from handlers import (
    start,
    callback,
    chat_actions,
    fsm_form, reference_menu, news_menu,
)
from scraper.async_mamba import AsyncMambaScraper


async def job():
    scraper = AsyncMambaScraper()
    await scraper.parse_pages()


async def scheduler(interval, func):
    while True:
        await func()
        await asyncio.sleep(interval)


async def on_startup(_):
    db = Database()
    db.sql_create_tables()
    asyncio.create_task(scheduler(300 / 5, job))


start.register_start_handlers(dp=dp)
callback.register_callback_handlers(dp=dp)
fsm_form.register_fsm_form_handlers(dp=dp)
reference_menu.register_reference_menu_handlers(dp=dp)
news_menu.register_news_menu_handlers(dp=dp)
chat_actions.register_chat_actions_handlers(dp=dp)

if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )
