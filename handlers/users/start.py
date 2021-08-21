from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from loader import dp, log

from keyboards.default.defaults import do_registration
from keyboards.dispatcher import dispatcher


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
