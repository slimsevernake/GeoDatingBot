from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.filters import BoundFilter

from typing import Union

from data.config import ADMINS


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: Union[Message, CallbackQuery]) -> bool:
        return str(message.from_user.id) in ADMINS
