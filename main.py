from aiogram import executor

from config import dp
from database.sql_commands import Database
from handlers import start, callback


async def on_startup(_):
    db = Database()
    db.sql_create_tables()


start.register_start_handlers(dp=dp)
callback.register_callback_handlers(dp=dp)

if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )
