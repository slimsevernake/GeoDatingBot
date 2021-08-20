from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from loader import dp

from keyboards.default.defaults import do_registration
from keyboards.dispatcher import dispatcher


@dp.message_handler(Text(equals=['Back']))
async def back(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyboard, prev_level = await dispatcher(data.get('prev_level', 'LEVEL_1'))
        message_text = 'Back to previous level'
        await message.answer(message_text, reply_markup=keyboard)
        data['prev_level'] = prev_level  # ALWAYS save new prev_level to state


@dp.message_handler(CommandStart(), state='*')
async def bot_start(m: types.Message, state: FSMContext):
    await m.answer(f"Привет, {m.from_user.full_name}!\n" +
                   'Пожалуйста, пройдите форму регистрации.',
                   reply_markup=do_registration)
    await state.finish()
