from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp

from keyboards.default.defaults import do_registration


@dp.message_handler(CommandStart(), state='*')
async def bot_start(m: types.Message, state: FSMContext):
    await m.answer(f"Привет, {m.from_user.full_name}!\n" +
                   'Пожалуйста, пройдите форму регистрации.',
                   reply_markup=do_registration)
    await state.finish()
