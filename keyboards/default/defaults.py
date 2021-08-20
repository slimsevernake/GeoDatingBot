from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


geo_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Share location', request_location=True)
)


user_info_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Gender'), KeyboardButton('Age')
).add(
    KeyboardButton('Interested gender'), KeyboardButton('Description')
).add(
    KeyboardButton('Location'), KeyboardButton('Search radius')
).add(
    KeyboardButton('Photo')
).add(
    KeyboardButton('Save')
).add(
    KeyboardButton('Back')
)


do_registration = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Sign up')
)
