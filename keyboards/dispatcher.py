#  https://github.com/Chenger1/Telegram-MultilevelKeyboard

from typing import Optional

from keyboards.default import menu

#  We cant store levels in 'flat' dict. Because in this case it would much harder to implement SINGLE 'Back' button
menu_storage = {
    'LEVEL_1': menu.level_1
}


async def dispatcher(level: str) -> tuple[menu.ReplyKeyboardMarkup, str]:
    """ Returns right keyboard for each level
        You can modify it in different purposes.
        For example if you want to have several user groups
        You can get user_id as parameter and checks his group, etc.
    """
    keyboard_cor, prev_level = await find_in_dict(level, menu_storage)
    return keyboard_cor, prev_level


async def find_in_dict(level: str, storage: dict, prev_level: str = 'LEVEL_1') \
        -> Optional[tuple[menu.ReplyKeyboardMarkup, str]]:
    """
    RECURSIVE function
    Iterates over storage. If key == level - return level`s keyboard
    If not and value is dict - pass it to recursion function. Dictionary is a sublevel.
    So, we run recursive coroutine and pass - level, THIS KEY`S VALUE - that is i mean sublevel
    And current prev_level.
    If this coroutine returns result - return it on top. Otherwise continue iteration
    :param level: Level we want to reach
    :param storage: menu_storage
    :param prev_level: name of previous menu level
    """

    for key, value in storage.items():
        if key == level:
            return value, prev_level.split(':')[0]  # for example: 'LEVEL_1:LEVEL_2' split by ':' to get 'LEVEL_1'
        if isinstance(value, dict):
            result = await find_in_dict(level, value, key)
            if result:
                return result
