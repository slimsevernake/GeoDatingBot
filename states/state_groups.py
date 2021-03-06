from aiogram.dispatcher.filters.state import State, StatesGroup


class UserInfoState(StatesGroup):
    starter = State()
    age = State()
    gender = State()
    interested_gender = State()
    photo = State()
    description = State()
    geolocation = State()
    search_distance = State()
    save = State()


class Mailing(StatesGroup):
    text = State()


class ListProfiles(StatesGroup):
    confirm = State()
    main = State()


class CustomUser(StatesGroup):
    coord = State()
