from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


level_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Display users')
).add(
    KeyboardButton('Edit info')
)


level_2_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Broadcast mailing'),
    KeyboardButton('Statistic')
).add(
    KeyboardButton('Back')
)
