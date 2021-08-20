from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


level_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Смотреть пользователей')
).add(
    KeyboardButton('Редактировать информацию')
)
