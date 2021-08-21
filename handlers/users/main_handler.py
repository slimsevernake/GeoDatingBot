from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils import exceptions
from loader import dp, log

from keyboards.inline.user_info_keyboard import confirm_keyboard, item_cb, get_user_profile_keyboard, like_dislike_cb
from keyboards.dispatcher import dispatcher

from db.models import User, Rate
from handlers.users.utils import prepare_user_profile

from states.state_groups import ListProfiles


async def get_user_info(user_id: int, index: int, me: int) -> tuple[str, str, types.InlineKeyboardMarkup]:
    user_info, photo_id = await prepare_user_profile(user_id, me)
    keyboard = await get_user_profile_keyboard(user_id, index)
    return user_info, photo_id, keyboard


async def pair_likes(user: User, me: User, call: types.CallbackQuery):
    if Rate.filter(rate_owner=user, target=me, type=True).exists():
        try:
            await call.bot.send_message(chat_id=me.user_id,
                                        text=f'This user ({user.full_name}) is also liked you: @{user.username}')
            await call.bot.send_message(chat_id=user.user_id,
                                        text=f'You have been liked by: @{me.username} too. ({me.full_name})')
        except exceptions.ChatNotFound:
            log.info(f'{user.user_id} char was not found')
            await call.message.answer('You liked test user. So here may be a username of real user')


@dp.message_handler(Text(equals=['Remove dislikes']))
async def remove_dislikes(m: types.Message):
    user = await User.get(user_id=m.from_user.id)
    disliked = await Rate.filter(rate_owner=user, type=False)
    for u in disliked:
        await u.delete()
    await m.answer(f'{len(disliked)} dislikes was removed')


@dp.message_handler(Text(equals=['Display users']))
async def display_matched_users(m: types.Message, state: FSMContext):
    user = await User.get(user_id=m.from_user.id)
    matched_users = await user.find_matched_users()
    if not matched_users:
        await m.answer('There are no any users in this area. ')
        return
    log.info(f'Founded: {len(matched_users)} for {m.from_user.id}')
    await m.answer(f'Founded {len(matched_users)} users.\nDo you want to see their profiles?',
                   reply_markup=confirm_keyboard)
    await ListProfiles.confirm.set()
    await state.update_data(users_list=matched_users)


@dp.callback_query_handler(item_cb.filter(action='confirm'), state=ListProfiles.confirm)
async def confirm_list_profiles(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = bool(int(callback_data.get('value')))
    if not value:
        await state.finish()
        await call.answer('Canceled')
        return
    async with state.proxy() as data:
        users_list = data['users_list']
        menu_keyboard, prev_level = await dispatcher('LEVEL_2_PROFILES')
        data['prev_level'] = prev_level
        user_info, photo_id, keyboard = await get_user_info(users_list[0], 0, call.from_user.id)
        await call.bot.send_message(chat_id=call.from_user.id, text='Profiles: ', reply_markup=menu_keyboard)
        await call.bot.send_photo(photo=photo_id, caption=user_info, reply_markup=keyboard,
                                  chat_id=call.from_user.id)
        await call.answer()
        await ListProfiles.main.set()


@dp.callback_query_handler(item_cb.filter(action='get_page'), state=ListProfiles.main)
async def get_profiles_page(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    index = int(callback_data.get('value', 0))
    async with state.proxy() as data:
        users_list = data['users_list']
        if not users_list:
            await call.message.delete()
            await call.bot.send_message(chat_id=call.from_user.id, text='There are not users')
        if index < 0 or index > len(users_list)-1:
            await call.answer('There is no page')
            return
        user_info, photo_id, keyboard = await get_user_info(users_list[index], index, call.from_user.id)
        await call.message.edit_media(
            types.input_media.InputMediaPhoto(media=photo_id, caption=user_info),
            reply_markup=keyboard)
        await call.answer()


@dp.callback_query_handler(like_dislike_cb.filter(action='like_dislike'), state=ListProfiles.main)
async def like_dislike(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data['user_id']
    action_type = bool(int(callback_data['type']))
    index = int(callback_data['index'])
    me = await User.get(user_id=call.from_user.id)
    user = await User.get(user_id=user_id)

    async with state.proxy() as data:
        users_list = data['users_list']
        if action_type:
            await Rate.create(rate_owner=me, target=user, type=True)
            await call.answer('Liked')
            index = index + 1 if index < len(users_list)-1 else index - 1

            await pair_likes(user, me, call)
        else:
            rate = await Rate.filter(rate_owner=me, target=user, type=True).first()
            if rate:
                await rate.delete()
            await Rate.create(rate_owner=me, target=user, type=False)
            await call.answer('Disliked')
            data['users_list'].pop(index)
        if not users_list:
            await call.message.delete()
            await call.bot.send_message(chat_id=call.from_user.id, text='There are no users more')
        user_info, photo_id, keyboard = await get_user_info(users_list[index], index, call.from_user.id)
        await call.message.edit_media(
            types.input_media.InputMediaPhoto(media=photo_id, caption=user_info),
            reply_markup=keyboard)
