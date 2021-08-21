import asyncio
from db.models import User

from aiogram.types import Message
from aiogram.utils import exceptions
from keyboards.default.defaults import geo_keyboard
from loader import log


async def get_user_age(data: dict) -> str:
    if data.get('age'):
        text = f'Current age {data["age"]}.\nInput a new one'
    else:
        text = 'Input your age'
    return text


async def get_user_gender(data: dict, key) -> str:
    if data.get(key):
        gender = await User.get_gender_display(data[key])
        text = f'Current gender: <b>{gender}</b>.\nChoose a new one'
    else:
        if key == 'gender':
            text = 'Choose gender'
        else:
            text = 'Choose interested gender'
    return text


async def get_user_photo(data: dict, m: Message):
    if data.get('photo'):
        await m.bot.send_photo(photo=data['photo'], chat_id=m.from_user.id,
                               caption='Current profile photo')
    else:
        await m.answer('Add profile photo')


async def get_user_description(data: dict) -> str:
    if data.get('description'):
        text = 'Current description: \n' + data['description']
    else:
        text = 'Add profile description'
    return text


async def get_user_location(data: dict, m: Message):
    if data.get('longitude') and data.get('latitude'):
        longitude = data['longitude']
        latitude = data['latitude']
        message = await m.answer('Current location.\nChoose a new one',
                                 reply_markup=geo_keyboard)
        await m.bot.send_location(chat_id=m.from_user.id,
                                  longitude=longitude, latitude=latitude,
                                  reply_to_message_id=message.message_id)
    else:
        await m.answer('Share location', reply_markup=geo_keyboard)


async def get_user_search_radius(data: dict) -> str:
    if data.get('search_distance'):
        text = f'Current radius: <b>{data["search_distance"]}</b>.\n' + \
               'Input new radius. In metre'
    else:
        text = 'Input radius. In metre'
    return text


async def send_message(user_id: int, text: str, bot) -> bool:
    try:
        await bot.send_message(user_id, text)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text, bot)
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.error(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def prepare_user_profile(user_id: int) -> tuple[str, str]:
    user = await User.get(user_id=user_id)
    text = f'<b>{user.username}</b>\n' + \
           f'<b>Age:</b> {user.age}\n' + \
           f'<b>Gender:</b> {await User.get_gender_display(user.gender)}\n\n' + \
           f'{user.description}\n' + \
           f'<b>Interesting: </b> {await User.get_gender_display(user.interested_gender)}'
    return text, user.photo
