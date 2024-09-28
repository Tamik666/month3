import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""SELECT * FROM products""").fetchall()
    conn.close()
    return products

async def start_sending_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)

    show_all_products = InlineKeyboardButton(text="Show All Products", callback_data="show_all_products")

    keyboard.add(show_all_products)
    await message.answer(text="Press to see goods", reply_markup=keyboard)

async def send_all_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()
    if products:
        for product in products:
            caption = (f"Name: {product['name_product']}\n"
                       f"Category: {product['category']}\n"
                       f"Size: {product['size']}\n"
                       f"Price: {product['price']}\n"
                       f"Art: {product['art']}\n")
            await callback_query.message.answer_photo(photo=product["photo"], caption=caption)
    else:
        await callback_query.message.answer("No products found")

def register_send_products(dp: Dispatcher):
    dp.register_message_handler(start_sending_products, commands=["products"])
    dp.register_callback_query_handler(send_all_products, Text(equals="show_all_products"))