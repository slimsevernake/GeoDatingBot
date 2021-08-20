import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage

from data import config

from tortoise import Tortoise

from logger import get_logger


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage('localhost', 6379, db=5)
dp = Dispatcher(bot, storage=storage)
db = Tortoise()
log = get_logger()

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    filemode='app.log', level=logging.INFO)

TORTOISE_ORM = {
    'connections': {'default': {
        'engine': 'tortoise.backends.asyncpg',
        'credentials': {
            'database': config.DB_NAME,
            'host': '127.0.0.1',
            'password': config.DB_PASSWORD,
            'port': '5432',
            'user': config.DB_USER
        }
    }},
    'apps': {
        'models': {
            'models': ['db.models', 'aerich.models'],
            'default_connection': 'default'
        }
    }
}
