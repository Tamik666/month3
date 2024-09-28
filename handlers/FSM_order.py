from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import buttons
from config import staff, bot
from db import db_main


class FSM_order(StatesGroup):
    art = State()
    size = State()
    quantity = State()
    contacts = State()
    submit = State()

async def start_fsm_order(message: types.Message):
    available_arts = db_main.get_available_arts()

    if not available_arts:
        await message.answer("No available arts.")
        return

    arts_list = "\n".join(available_arts)
    await message.answer(f"Available arts:\n"
                         f"{arts_list}\n"
                         f"Please enter art: ", reply_markup=buttons.cancel_button)
    await FSM_order.art.set()


async def load_art(message: types.Message, state: FSMContext):
    art = message.text
    art_stock = db_main.get_available_arts()
    if not db_main.check_art_exists(art):
        await message.answer(f"Art not found in the database. Please enter a valid art.\n"
                             f"For example {art_stock}")
        return

    async with state.proxy() as data:
        data['art'] = art
        size_quantity = db_main.check_size_available(art)

    size_buttons = InlineKeyboardMarkup(row_width=3)
    sizes = ['S', 'M', 'L', 'XL', 'XXL', '3XL']
    size_buttons.add(*[InlineKeyboardButton(size, callback_data=size) for size in sizes])

    await FSM_order.next()
    await message.answer(f"Choose sizes:\n"
                         f"In stock only {size_quantity} sizes", reply_markup=size_buttons)


async def load_size(callback_query: types.CallbackQuery, state: FSMContext):
    size = callback_query.data

    if not db_main.check_size_stock(size):
        await callback_query.message.answer("Size not found in the database. Please enter a valid size.")
        return

    async with state.proxy() as data:
        data['size'] = size
        stock_quantity = db_main.check_product_stock(data['art'])

    await callback_query.message.answer(f'Quantity between 1 and {int(stock_quantity)}:',
                                        reply_markup=ReplyKeyboardRemove())
    await FSM_order.next()


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            quantity = int(message.text)
        except ValueError:
            await message.answer("Please enter a valid quantity.")
            return

        stock_quantity = db_main.check_product_stock(data['art'])

        if quantity > int(stock_quantity):
            await message.answer(
                f"In store only {stock_quantity} in stock. Please select between 1 and {stock_quantity}.")
            return

        data['quantity'] = quantity

    await message.answer("Contacts:")
    await FSM_order.next()


async def load_contacts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contacts'] = message.text

    await message.answer(f"True?\n"
                         f"Art: {data['art']}\n"
                         f"Size: {data['size']}\n"
                         f"Quantity: {data['quantity']}\n"
                         f"Contact info: {data['contacts']}",
                         reply_markup=buttons.submit_button)
    await FSM_order.submit.set()


async def submit_order(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()
    if message.text.lower() == "yes":
        async with state.proxy() as data:
            staff_message = (f"New order received:\n"
                             f"Art: {data['art']}\n"
                             f"Size: {data['size']}\n"
                             f"Quantity: {data['quantity']}\n"
                             f"Contact info: {data['contacts']}")
            for staff_id in staff:
                await bot.send_message(chat_id=staff_id, text=staff_message)
        await message.answer("Order submitted successfully!", reply_markup=kb)
        await state.finish()
    elif message.text.lower() == "no":
        await message.answer("Ordering aborted!", reply_markup=kb)
        await state.finish()
    else:
        await message.answer("Invalid input! Please type 'yes' or 'no'.")


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    kb = ReplyKeyboardRemove()
    if current_state is not None:
        await state.finish()
        await message.answer('Cancelled!', reply_markup=kb)


def register_fsm_order(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Cancel', ignore_case=True), state="*")
    dp.register_message_handler(start_fsm_order, commands=['order'])
    dp.register_message_handler(load_art, state=FSM_order.art)
    dp.register_callback_query_handler(load_size, state=FSM_order.size)
    dp.register_message_handler(load_quantity, state=FSM_order.quantity)
    dp.register_message_handler(load_contacts, state=FSM_order.contacts)
    dp.register_message_handler(submit_order, state=FSM_order.submit)