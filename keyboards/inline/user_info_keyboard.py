from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callbacks import item_cb

gender_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Man', callback_data=item_cb.new(action='choose_gender',
                                                          value=1,
                                                          second_value=False)),
    InlineKeyboardButton('Woman', callback_data=item_cb.new(action='choose_gender',
                                                            value=0,
                                                            second_value=False))
)

confirm_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Confirm', callback_data=item_cb.new(action='confirm',
                                                              value=1,
                                                              second_value=False)),
    InlineKeyboardButton('Cancel', callback_data=item_cb.new(action='confirm',
                                                             value=0,
                                                             second_value=False))
)
