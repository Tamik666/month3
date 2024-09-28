from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add(KeyboardButton("/start"),
                                                                        KeyboardButton("/info"),
                                                                        KeyboardButton("/products"),
                                                                        KeyboardButton("/store"),
                                                                        KeyboardButton("/order"))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Cancel'))

submit_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                    row_width=2).add(KeyboardButton('Yes'), KeyboardButton('No'))