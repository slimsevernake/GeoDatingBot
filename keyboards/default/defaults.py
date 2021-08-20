from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


geo_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить геолокацию', request_location=True)
)


user_info_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Пол'), KeyboardButton('Возраст')
).add(
    KeyboardButton('Интересующий пол'), KeyboardButton('Описание')
).add(
    KeyboardButton('Локация'), KeyboardButton('Радиус поиска')
).add(
    KeyboardButton('Фото')
).add(
    KeyboardButton('Сохранить')
).add(
    KeyboardButton('Вернуться')
)


do_registration = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Зарегестрироваться')
)
