from db.models import User

from aiogram.types import Message
from keyboards.default.defaults import geo_keyboard


async def get_user_age(data: dict) -> str:
    if data.get('age'):
        text = f'Текущий возраст {data["age"]}.\nВведите новый'
    else:
        text = 'Введите ваш возраст'
    return text


async def get_user_gender(data: dict, key) -> str:
    if data.get(key):
        gender = await User.get_gender_display(data[key])
        text = f'Текущий пол: <b>{gender}</b>.\nВыберите новый'
    else:
        if key == 'gender':
            text = 'Выберите пол'
        else:
            text = 'Выберите интересующий пол'
    return text


async def get_user_photo(data: dict, m: Message):
    if data.get('photo'):
        await m.delete()
        await m.bot.send_photo(photo=data['photo'], chat_id=m.from_user.id,
                               caption='Текущее фото профиля')
    else:
        await m.answer('Добавьте фото профиля')


async def get_user_description(data: dict) -> str:
    if data.get('description'):
        text = 'Текущее описание: \n' + data['description']
    else:
        text = 'Добавьте описание профиля'
    return text


async def get_user_location(data: dict, m: Message):
    if data.get('longitude') and data.get('latitude'):
        longitude = data['longitude']
        latitude = data['latitude']
        message = await m.answer('Текущее местоположение.\nВыберите новое',
                                 reply_markup=geo_keyboard)
        await m.bot.send_location(chat_id=m.from_user.id,
                                  longitude=longitude, latitude=latitude,
                                  reply_to_message_id=message.message_id)
    else:
        await m.answer('Выберите локацию', reply_markup=geo_keyboard)


async def get_user_search_radius(data: dict) -> str:
    if data.get('search_distance'):
        text = f'Текущий радиус: <b>{data["search_distance"]}</b>.\n' + \
               'Введите новый'
    else:
        text = 'Введите радиус поиска'
    return text
