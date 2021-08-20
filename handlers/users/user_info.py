from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher import FSMContext

from loader import dp
from states.state_groups import UserInfoState

from keyboards.default.defaults import user_info_keyboard
from keyboards.inline.user_info_keyboard import gender_keyboard, confirm_keyboard
from keyboards.callbacks import item_cb

from db.models import User
from handlers.users import utils


user_info_keys = {'user_id', 'username', 'description', 'gender', 'interested_gender',
                  'age', 'longitude', 'latitude', 'search_distance', 'photo'}


async def user_dict_info_to_text(data: dict) -> str:
    gender = await User.get_gender_display(data['gender'])
    interested_gender = await User.get_gender_display(data['interested_gender'])
    age_suffix = await User.get_age_suffix(data['age'])
    text = f'Возраст: <b>{data["age"]}</b> {age_suffix}\n' + \
           f'Пол: <b>{gender}</b>\n' + \
           f'Интересующий пол: <b>{interested_gender}</b>\n' + \
           f'Радиус поиска: <b>{data["search_distance"]}</b>\n\n' + \
           f'{data["description"]}'
    return text


@dp.message_handler(Text(equals=['Вернуться']), state=UserInfoState)
async def back_button(m: types.Message, state: FSMContext):
    user = await User.get_or_none(user_id=m.from_user.id)
    if not user:
        await m.delete()
        await m.bot.send_message(chat_id=m.from_user.id, text='Сперва закончите регистрацию')
        return
    data = await state.get_data()
    await state.finish()
    data.pop('user')
    await state.update_data(**data)


@dp.message_handler(Text(equals=['Возраст']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_age(data['user'])
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text)
    await UserInfoState.age.set()


@dp.message_handler(Text(equals=['Пол']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_gender(data['user'], 'gender')
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text, reply_markup=gender_keyboard)
    await UserInfoState.gender.set()


@dp.message_handler(Text(equals=['Интересующий пол']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_gender(data['user'], 'interested_gender')
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text, reply_markup=gender_keyboard)
    await UserInfoState.interested_gender.set()


@dp.message_handler(Text(equals=['Описание']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_description(data['user'])
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text)
    await UserInfoState.description.set()


@dp.message_handler(Text(equals=['Локация']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    await utils.get_user_location(data['user'], m)
    await UserInfoState.geolocation.set()


@dp.message_handler(Text(equals=['Радиус поиска']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_search_radius(data['user'])
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text)
    await UserInfoState.search_distance.set()


@dp.message_handler(Text(equals=['Фото']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    await utils.get_user_photo(data, m)
    await UserInfoState.photo.set()


@dp.message_handler(Text(equals=['Сохранить']), state=UserInfoState)
async def send_confirm_to_save(m: types.Message, state: FSMContext):
    data = await state.get_data()
    user_dict_data_keys = set(data['user'].keys())
    if user_dict_data_keys ^ user_info_keys:
        await m.delete()
        await m.bot.send_message(chat_id=m.from_user.id, text='Введены не все данные')
        return

    text = await user_dict_info_to_text(data['user'])
    text += '\n<b>Подтверждаете?</b>'
    await m.delete()
    await m.bot.send_location(chat_id=m.from_user.id,
                              latitude=data['user']['latitude'],
                              longitude=data['user']['longitude'])
    await m.bot.send_photo(chat_id=m.from_user.id,
                           photo=data['user']['photo'],
                           caption=text,
                           reply_markup=confirm_keyboard)


@dp.message_handler(Text(equals=['Зарегестрироваться', 'Изменить данные']))
async def user_info_base_handler(m: types.Message, state: FSMContext):
    await UserInfoState.starter.set()
    user = await User.get_or_none(user_id=m.from_user.id)
    if user:
        async with state.proxy() as data:
            data['user'] = {
                'user_id': user.user_id,
                'username': user.username,
                'description': user.description,
                'gender': user.gender,
                'interested_gender': user.interested_gender,
                'age': user.age,
                'longitude': user.longitude,
                'latitude': user.latitude,
                'search_distance': user.search_distance,
                'photo': user.photo
            }
        await m.answer('Выберите какие данные нужно изменить через меню', reply_markup=user_info_keyboard)
    else:
        text = 'Укажите свой возраст.\n Вам не может быть меньше 18.'
        await m.answer(f"Привет, {m.from_user.full_name}!\n" +
                       'Пожалуйста, пройдите форму регистрации.',
                       reply_markup=user_info_keyboard)
        async with state.proxy() as data:
            data['user'] = {
                'user_id': m.from_user.id,
                'username': m.from_user.full_name
            }
            data['creating'] = True
        await m.answer(text)
        await UserInfoState.age.set()


@dp.message_handler(state=UserInfoState.age)
async def choose_user_age(m: types.Message, state: FSMContext):
    age = m.text
    try:
        age = int(age)
        if age < 18:
            await m.answer('Вам не может быть меньше 18')
        elif age >= 100:
            await m.answer('Вам не может быть больше 100')
        else:
            async with state.proxy() as data:
                data['user']['age'] = age
                if data.get('creating'):
                    text = await utils.get_user_gender(data['user'], 'gender')
                    await m.answer(text, reply_markup=gender_keyboard)
                    await UserInfoState.gender.set()
                else:
                    await m.answer('Сохранено')
    except ValueError:
        await m.answer('Неправильный формат ввода')


@dp.callback_query_handler(item_cb.filter(action='choose_gender'), state=UserInfoState.gender)
async def choose_user_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data.get('value')
    async with state.proxy() as data:
        data['user']['gender'] = bool(int(value))  # callback returns data as a string
        #  Bool value like True will return like 'True' - as a string. So i store is as a integer
        await call.answer('Сохранено')
        if data.get('creating'):
            text = await utils.get_user_gender(data['user'], 'interested_gender')
            await call.message.answer(text, reply_markup=gender_keyboard)
            await UserInfoState.interested_gender.set()


@dp.callback_query_handler(item_cb.filter(action='choose_gender'), state=UserInfoState.interested_gender)
async def choose_user_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data.get('value')
    async with state.proxy() as data:
        data['user']['interested_gender'] = bool(int(value))
        await call.answer('Сохранено')
        if data.get('creating'):
            await utils.get_user_photo(data['user'], call.message)
            await UserInfoState.photo.set()


@dp.message_handler(state=UserInfoState.photo, content_types=types.ContentType.PHOTO)
async def profile_photo(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user']['photo'] = m.photo[-1].file_id
        if data.get('creating'):
            text = await utils.get_user_description(data['user'])
            await m.answer(text)
            await UserInfoState.description.set()
        else:
            await m.answer('Сохранено')


@dp.message_handler(state=UserInfoState.description)
async def add_profile_description(m: types.Message, state: FSMContext):
    if len(m.text) <= 30:
        await m.answer('Описание слишком короткое')
    else:
        async with state.proxy() as data:
            data['user']['description'] = m.text
            if data.get('creating'):
                await utils.get_user_location(data['user'], m)
                await UserInfoState.geolocation.set()
            else:
                await m.answer('Сохранено')


@dp.message_handler(state=UserInfoState.geolocation, content_types=['location'])
async def profile_location(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user']['longitude'] = m.location.longitude
        data['user']['latitude'] = m.location.latitude
        if data.get('creating'):
            text = await utils.get_user_search_radius(data['user'])
            await m.answer(text, reply_markup=user_info_keyboard)
            await UserInfoState.search_distance.set()
        else:
            await m.answer('Сохранено')


@dp.message_handler(state=UserInfoState.search_distance)
async def search_distance(m: types.Message, state: FSMContext):
    try:
        radius = int(m.text)
        if radius < 30:
            await m.answer('Радиус слишком маленький')
        elif radius >= 10000:
            await m.answer('Радиус слишком большой')
        else:
            async with state.proxy() as data:
                data['user']['search_distance'] = radius
            if data.get('creating'):
                await m.answer('Все данные добавлены. Вы можете изменить их или сохранить')
            else:
                await m.answer('Сохранено')
    except ValueError:
        await m.answer('Неправильный формат ввода')


@dp.callback_query_handler(item_cb.filter(action='confirm'), state=UserInfoState)
async def save_user(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = bool(int(callback_data.get('value')))
    if value:
        await call.answer()
        async with state.proxy() as data:
            user_data = data['user']
            user, created = await User.get_or_create(user_id=call.from_user.id,
                                                     defaults={'username': user_data['username'],
                                                               'description': user_data['description'],
                                                               'gender': user_data['gender'],
                                                               'interested_gender': user_data['interested_gender'],
                                                               'age': int(user_data['age']),
                                                               'longitude': float(user_data['longitude']),
                                                               'latitude': float(user_data['latitude']),
                                                               'search_distance': user_data['search_distance'],
                                                               'photo': user_data['photo'],
                                                               'age_suffix': await User.get_age_suffix(user_data['age'])})
            if created:
                await call.message.answer('Добро пожаловать')
            else:
                for key, value in user_data.items():
                    setattr(user, key, value)
                try:
                    user.age_suffix = await User.get_age_suffix(user.age)
                    await user.save()
                except Exception as e:
                    await call.message.answer(str(e))
                else:
                    await call.message.answer('Данные изменены')
            data.pop('user')
            await state.finish()
    else:
        await call.answer('Вы можете выбрать нужный этап через меню', show_alert=True)
