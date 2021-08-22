import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from loader import dp, log

from keyboards.dispatcher import dispatcher
from keyboards.inline.user_info_keyboard import get_request_to_admin_keyboard, item_cb

from states.state_groups import Mailing

from db.models import User, RequestToAdmin
from db.statistic import Statistic
from handlers.users.utils import send_message
from data.config import add_to_admin_list


stat: Statistic = Statistic()


@dp.message_handler(commands=['admin'], is_admin=True)
async def admin_panel(m: types.Message, state: FSMContext):
    log.info(f'User {m.from_user.id} has access to admin panel')
    keyboard, prev_level = await dispatcher('LEVEL_2_ADMIN')
    await m.answer('Admin panel', reply_markup=keyboard)
    await state.update_data(prev_level=prev_level)


@dp.message_handler(Text(equals=['Broadcast mailing']), is_admin=True)
async def mailing(m: types.Message):
    await Mailing.text.set()
    await m.answer('Input message for all users')


@dp.message_handler(state=Mailing.text)
async def broadcast(m: types.Message, state: FSMContext):
    count = 0
    try:
        for user in await User.all():
            if await send_message(user.user_id, m.text, m.bot):
                count += 1
            await asyncio.sleep(.05)
    finally:
        await m.answer(f'{count} messages successful sent.')
    state_data = await state.get_data()
    await state.finish()
    await state.update_data(**state_data)


@dp.message_handler(Text(equals=['Statistic']), is_admin=True)
async def statistic_menu(m: types.Message):
    statistic_data = await stat.report()
    log.info(f'User {m.from_user.id} requests statistic')
    log.info(statistic_data)
    text = ''
    for key, value in statistic_data.items():
        text += f'<b>{key}</b>: {value or 0}\n'
    await m.answer(text)


@dp.message_handler(Text(equals=['Logs']), is_admin=True)
async def get_logs(m: types.Message):
    log.info(f'User: {m.from_user.id} - gets logs')
    with open('app.log', 'rb') as file:
        await m.bot.send_document(chat_id=m.from_user.id, document=file,
                                  caption='Log file')


@dp.message_handler(Text(equals=['Requests to admin']), is_admin=True)
async def requests_to_admin(m: types.Message):
    requests = await RequestToAdmin.all()
    for req in requests:
        await req.fetch_related('user')
        keyboard = await get_request_to_admin_keyboard(req.user.user_id)
        await m.answer(f'User {req.user.full_name} - @{req.user.username}', reply_markup=keyboard)


@dp.callback_query_handler(item_cb.filter(action='request_to_admin'), is_admin=True)
async def confirm_request(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get('value')
    action = bool(int(callback_data.get('second_value')))
    await (await RequestToAdmin.get(user__user_id=user_id)).delete()
    if action:
        await add_to_admin_list(user_id)
        await call.bot.send_message(chat_id=user_id, text='You are admin already')
        log.info(f'User {user_id} is admin now')
        await call.bot.send_message(chat_id=user_id, text='You request to admin approved. Yor are <b>admin</b> now')
    else:
        log.info(f'Request from {user_id} was disapproved')
        await call.bot.send_message(chat_id=user_id, text='You request to admin was disapproved')
