from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher import FSMContext

from loader import dp, log
from states.state_groups import UserInfoState

from keyboards.default.defaults import user_info_keyboard
from keyboards.inline.user_info_keyboard import gender_keyboard, confirm_keyboard
from keyboards.callbacks import item_cb
from keyboards.dispatcher import dispatcher

from db.models import User
from handlers.users import utils


user_info_keys = {'user_id', 'username', 'description', 'gender', 'interested_gender',
                  'age', 'longitude', 'latitude', 'search_distance', 'photo'}


async def user_dict_info_to_text(data: dict) -> str:
    gender = await User.get_gender_display(data['gender'])
    interested_gender = await User.get_gender_display(data['interested_gender'])
    text = f'Age: <b>{data["age"]}</b> years old\n' + \
           f'Gender: <b>{gender}</b>\n' + \
           f'Interested gender: <b>{interested_gender}</b>\n' + \
           f'Search radius: <b>{data["search_distance"]}</b> м.\n\n' + \
           f'{data["description"]}'
    return text


@dp.message_handler(Text(equals=['Back']), state=UserInfoState)
async def back_button(m: types.Message, state: FSMContext):
    user = await User.get_or_none(user_id=m.from_user.id)
    if not user:
        await m.answer('Finish the registration first')
        return
    data = await state.get_data()
    await state.finish()
    keyboard, prev_level = await dispatcher('LEVEL_1')
    data.pop('user')
    data['prev_level'] = prev_level
    await state.update_data(**data)
    await m.answer('Returning...', reply_markup=keyboard)


@dp.message_handler(Text(equals=['Age']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_age(data['user'])
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text)
    await UserInfoState.age.set()


@dp.message_handler(Text(equals=['Gender']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_gender(data['user'], 'gender')
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text, reply_markup=gender_keyboard)
    await UserInfoState.gender.set()


@dp.message_handler(Text(equals=['Interested gender']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_gender(data['user'], 'interested_gender')
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text, reply_markup=gender_keyboard)
    await UserInfoState.interested_gender.set()


@dp.message_handler(Text(equals=['Description']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_description(data['user'])
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text)
    await UserInfoState.description.set()


@dp.message_handler(Text(equals=['Location']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    await utils.get_user_location(data['user'], m)
    await UserInfoState.geolocation.set()


@dp.message_handler(Text(equals=['Search radius']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await utils.get_user_search_radius(data['user'])
    await m.delete()
    await m.bot.send_message(chat_id=m.from_user.id, text=text)
    await UserInfoState.search_distance.set()


@dp.message_handler(Text(equals=['Photo']), state=UserInfoState)
async def user_gender(m: types.Message, state: FSMContext):
    data = await state.get_data()
    await utils.get_user_photo(data, m)
    await UserInfoState.photo.set()


@dp.message_handler(Text(equals=['Save']), state=UserInfoState)
async def send_confirm_to_save(m: types.Message, state: FSMContext):
    data = await state.get_data()
    user_dict_data_keys = set(data['user'].keys())
    difference = user_dict_data_keys ^ user_info_keys
    if difference:
        text = 'Some data were not passed' + \
                '.'.join(difference)
        await m.answer(text)
        return

    text = await user_dict_info_to_text(data['user'])
    text += '\n<b>Confirm?</b>'
    await m.delete()
    await m.bot.send_location(chat_id=m.from_user.id,
                              latitude=data['user']['latitude'],
                              longitude=data['user']['longitude'])
    await m.bot.send_photo(chat_id=m.from_user.id,
                           photo=data['user']['photo'],
                           caption=text,
                           reply_markup=confirm_keyboard)


@dp.message_handler(Text(equals=['Sign up', 'Edit info']))
async def user_info_base_handler(m: types.Message, state: FSMContext):
    await UserInfoState.starter.set()
    user = await User.get_or_none(user_id=m.from_user.id)
    if user:
        log.info(f'User {m.from_user.id} edit info')
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
            data['creating'] = False
        await m.answer('Use menu to choose data to change', reply_markup=user_info_keyboard)
    else:
        text = 'Input you age.\nYou cant be youngest than 18.'
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
            await m.answer('You cant be youngest than 18')
        elif age >= 100:
            await m.answer('You cant be older than 100')
        else:
            async with state.proxy() as data:
                data['user']['age'] = age
                if data.get('creating'):
                    text = await utils.get_user_gender(data['user'], 'gender')
                    await m.answer(text, reply_markup=gender_keyboard)
                    await UserInfoState.gender.set()
                else:
                    await m.answer('Saved')
    except ValueError:
        await m.answer('Wrong format')


@dp.callback_query_handler(item_cb.filter(action='choose_gender'), state=UserInfoState.gender)
async def choose_user_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data.get('value')
    async with state.proxy() as data:
        data['user']['gender'] = bool(int(value))  # callback returns data as a string
        #  Bool value like True will return like 'True' - as a string. So i store is as a integer
        await call.answer('Saved')
        if data.get('creating'):
            text = await utils.get_user_gender(data['user'], 'interested_gender')
            await call.message.answer(text, reply_markup=gender_keyboard)
            await UserInfoState.interested_gender.set()


@dp.callback_query_handler(item_cb.filter(action='choose_gender'), state=UserInfoState.interested_gender)
async def choose_user_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data.get('value')
    async with state.proxy() as data:
        data['user']['interested_gender'] = bool(int(value))
        await call.answer('Saved')
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
            await m.answer('Saved')


@dp.message_handler(state=UserInfoState.description)
async def add_profile_description(m: types.Message, state: FSMContext):
    if len(m.text) <= 30:
        await m.answer('Description is too short')
    else:
        async with state.proxy() as data:
            data['user']['description'] = m.text
            if data.get('creating'):
                await utils.get_user_location(data['user'], m)
                await UserInfoState.geolocation.set()
            else:
                await m.answer('Saved')


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
            await m.answer('Saved')


@dp.message_handler(state=UserInfoState.search_distance)
async def search_distance(m: types.Message, state: FSMContext):
    try:
        radius = int(m.text)
        if radius < 30:
            await m.answer('Radius is too small')
        elif radius >= 10000:
            await m.answer('Radius is too big')
        else:
            async with state.proxy() as data:
                data['user']['search_distance'] = radius
            if data.get('creating'):
                await m.answer('All data has been updated. You can change them or save')
            else:
                await m.answer('Saved')
    except ValueError:
        await m.answer('Wrong format')


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
                                                               'photo': user_data['photo']})
            if created:
                text = 'Welcome!'
            else:
                for key, value in user_data.items():
                    setattr(user, key, value)
                try:
                    await user.save()
                except Exception as e:
                    await call.message.answer(str(e))
                else:
                    text = 'Data has been changed'
            keyboard, prev_level = await dispatcher('LEVEL_1')
            await call.message.answer(text, reply_markup=keyboard)
            data.pop('user')
            data.pop('creating')
            data['prev_level'] = prev_level
            await state.finish()
    else:
        await call.answer('You can choose stage using menu', show_alert=True)
