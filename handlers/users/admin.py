from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from keyboards.dispatcher import dispatcher


@dp.message_handler(commands=['admin'], is_admin=True)
async def admin_panel(m: types.Message, state: FSMContext):
    keyboard, prev_level = await dispatcher('LEVEL_2_ADMIN')
    await m.answer('Admin panel', reply_markup=keyboard)
    await state.update_data(prev_level=prev_level)
