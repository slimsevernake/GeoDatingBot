from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


level_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Display users')
).add(
    KeyboardButton('Edit info'),
    KeyboardButton('Remove dislikes')
)


level_2_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Broadcast mailing'),
    KeyboardButton('Statistic')
).add(
    KeyboardButton('Back')
)


level_2_profiles = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Back')
)
