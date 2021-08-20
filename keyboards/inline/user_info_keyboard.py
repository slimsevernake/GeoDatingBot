from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callbacks import item_cb


gender_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Мужчина', callback_data=item_cb.new(action='choose_gender',
                                                              value=1,
                                                              second_value=False)),
    InlineKeyboardButton('Женщина', callback_data=item_cb.new(action='choose_gender',
                                                              value=0,
                                                              second_value=False))
)


confirm_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Подтвердить', callback_data=item_cb.new(action='confirm',
                                                                  value=1,
                                                                  second_value=False)),
    InlineKeyboardButton('Отменить', callback_data=item_cb.new(action='confirm',
                                                               value=0,
                                                               second_value=False))
)

