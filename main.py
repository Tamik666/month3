import logging
from aiogram.utils import executor
from buttons import start
from config import bot, dp, staff
from handlers import (commands, echo, FSM_store, FSM_order, send_products)
from db import db_main

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    for i in staff:
        await bot.send_message(chat_id=i, text="Bot is ready!", reply_markup=start)

    db_main.sql_create_products()

commands.register_commands(dp)
FSM_store.register_fsm_store(dp)
FSM_order.register_fsm_order(dp)
send_products.register_send_products(dp)
echo.register_echo(dp)

if __name__ == '__main__':
    logging.info("Bot is starting...")
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)