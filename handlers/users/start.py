from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from loader import dp, log

from keyboards.default.defaults import do_registration
from keyboards.dispatcher import dispatcher
from states.state_groups import CustomUser

from db.models import User, Rate

import random


@dp.message_handler(Text(equals=['Back']), state='*')
async def back(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await state.finish()
        keyboard, prev_level = await dispatcher(data.get('prev_level', 'LEVEL_1'))
        message_text = 'Back to previous level'
        await message.answer(message_text, reply_markup=keyboard)
        data['prev_level'] = prev_level  # ALWAYS save new prev_level to state


@dp.message_handler(CommandStart(), state='*')
async def bot_start(m: types.Message, state: FSMContext):
    await m.answer(f"Hello, {m.from_user.full_name}!\n" +
                   'Please, sign up first.',
                   reply_markup=do_registration)
    log.info(f'User: {m.from_user.id} comes')
    await state.finish()


@dp.message_handler(Text(equals=['Add custom user(For test only)']))
async def add_custom_user(m: types.Message, state: FSMContext):
    keyboard, prev_level = await dispatcher('LEVEL_2_PROFILES')
    text = 'Because testers live in different cities, it can be hard to test distance calculating.\n' + \
           'So you can create test user with custom coordinates for testing.\n' + \
           'This user will liked you\n' + \
           'Coordinates you can get from Google Maps for your city or any place you want\n\n' + \
           'Input coordinates in format - longitude:latitude'
    await m.answer(text, reply_markup=keyboard)
    await CustomUser.coord.set()
    await state.update_data(prev_level=prev_level)


@dp.message_handler(state=CustomUser.coord)
async def set_custom_user(m: types.Message, state: FSMContext):
    if ':' not in m.text:
        await m.answer('Wrong format')
        return
    lat, long = m.text.split(':')
    try:
        long, lat = float(long), float(lat)
        rand_id = random.randint(0, 10000)
        photo_id = 'AgACAgIAAxkBAAINLWEhJltMgCWIPVTZ_27n9ZgnVSLSAAICszEbpycISbTVoFhMhtIaAQADAgADeQADIAQ'
        user = await User.create(user_id=rand_id,
                                 full_name=f'Test {rand_id}',
                                 username=f'Test username {rand_id}',
                                 description=f'Test desc {rand_id}',
                                 gender=True,
                                 interested_gender=False,
                                 age=30,
                                 longitude=long, latitude=lat,
                                 search_distance=100000,
                                 photo=photo_id)
        me = await User.get(user_id=m.from_user.id)
        await Rate.create(rate_owner=user, target=me, type=True)
        await m.answer('Saved')
        data = await state.get_data()
        await state.finish()
        await state.update_data(**data)
    except ValueError:
        await m.answer('Wrong format')
        return
