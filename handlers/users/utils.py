from db.models import User

from aiogram.types import Message
from keyboards.default.defaults import geo_keyboard


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
