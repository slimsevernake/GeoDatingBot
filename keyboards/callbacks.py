from aiogram.utils.callback_data import CallbackData

item_cb = CallbackData('item', 'action', 'value', 'second_value')
like_dislike_cb = CallbackData('like_dislike', 'action', 'user_id', 'type', 'index')
