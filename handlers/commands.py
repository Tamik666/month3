from aiogram import types, Dispatcher

from  config import  bot

async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Hello!")

async def info_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Bot created for fill products info and for buy products")

def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(info_handler, commands=["info"])