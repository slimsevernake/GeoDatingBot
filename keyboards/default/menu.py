from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


level_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Display users'),
    KeyboardButton('Display liked users')
).add(
    KeyboardButton('Edit info'),
    KeyboardButton('Remove dislikes')
).add(
    KeyboardButton('Add custom user(For test only)')
)


level_2_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Broadcast mailing'),
    KeyboardButton('Statistic')
).add(
    KeyboardButton('Logs')
).add(
    KeyboardButton('Back')
)


level_2_profiles = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Back')
)
