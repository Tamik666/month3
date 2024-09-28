from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import buttons
from config import staff
from db import db_main

class FSM_store(StatesGroup):
    product_name = State()
    category = State()
    size = State()
    price = State()
    art = State()
    quantity = State()
    photo = State()
    submit = State()

async def start_fsm_store(message: types.Message):
    if message.from_user.id not in staff:
        await message.answer("you're not in staff")
    else:
        await message.answer("Product name:", reply_markup=buttons.cancel_button)
        await FSM_store.product_name.set()

async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer('Category:', reply_markup=ReplyKeyboardRemove())
    await FSM_store.next()

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    size_buttons = InlineKeyboardMarkup(row_width=3)
    sizes = ['S', 'M', 'L', 'XL', 'XXL', '3XL']
    size_buttons.add(*[InlineKeyboardButton(size, callback_data=size) for size in sizes])
    await FSM_store.next()
    await message.answer("Choose sizes:", reply_markup=size_buttons)

async def load_size(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = callback_query.data
    await callback_query.message.answer('Price:', reply_markup=ReplyKeyboardRemove())
    await FSM_store.next()

async def load_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        async with state.proxy() as data:
            data['price'] = price
        await message.answer("Art: ")
        await FSM_store.next()
    except ValueError:
        await message.answer("Please enter a valid price.")

async def load_art(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['art'] = message.text
    await message.answer("Quantity:")
    await FSM_store.next()

async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await message.answer("Photo: ")
    await FSM_store.next()

async def load_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo.")
        return
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await message.answer_photo(photo=data['photo'],
                               caption=f"True?\n"
                                       f"Name: {data['product_name']}\n"
                                       f"Category: {data['category']}\n"
                                       f"Size: {data['size']}\n"
                                       f"Price: {data['price']}\n"
                                       f"Art: {data['art']}\n"
                                       f"Quantity: {data['quantity']}\n",
                               reply_markup=buttons.submit_button)
    await FSM_store.submit.set()

async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()
    if message.text.lower() == "yes":
        async with state.proxy() as data:
            try:
                db_main.sql_insert_products(name_product=data['product_name'],
                                            category=data['category'],
                                            size=data['size'],
                                            price=data['price'],
                                            art=data['art'],
                                            quantity=data['quantity'],
                                            photo=data['photo'])
            except Exception as e:
                await message.answer(f"Error while saving product: {e}")
            else:
                await message.answer("Registration successful!", reply_markup=kb)
            await state.finish()
    elif message.text.lower() == "no":
        await message.answer("Registration aborted!", reply_markup=kb)
        await state.finish()
    else:
        await message.answer("Invalid input! Please type 'yes' or 'no'.")

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    kb = ReplyKeyboardRemove()
    if current_state is not None:
        await state.finish()
        await message.answer('Cancelled!', reply_markup=kb)

def register_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Cancel', ignore_case=True), state="*")
    dp.register_message_handler(start_fsm_store, commands=['store'])
    dp.register_message_handler(load_product_name, state=FSM_store.product_name)
    dp.register_message_handler(load_category, state=FSM_store.category)
    dp.register_callback_query_handler(load_size, state=FSM_store.size)
    dp.register_message_handler(load_price, state=FSM_store.price)
    dp.register_message_handler(load_art, state=FSM_store.art)
    dp.register_message_handler(load_quantity, state=FSM_store.quantity)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_store.photo)
    dp.register_message_handler(submit, state=FSM_store.submit)
