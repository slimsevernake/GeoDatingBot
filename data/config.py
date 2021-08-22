from environs import Env
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ADMINS = config['DEFAULT']['ADMINS'].split(',')

env = Env()
env.read_env()
BOT_TOKEN = env.str("BOT_TOKEN")
IP = env.str("ip")
DB_NAME = env.str('DB_NAME')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_USER = env.str('DB_USER')

DEBUG = bool(int(env.str('DEBUG')))
if DEBUG:
    REDIS_HOST = 'localhost'
    DB_HOST = '127.0.0.1'
else:
    REDIS_HOST = env.str('REDIS_HOST')
    DB_HOST = env.str('DB_HOST')


async def add_to_admin_list(user_id: str):
    """
        ADMINS data stores in memory, so append it.
        Also, write new ADMINS data to config.ini file for potential bot reboot
    """
    ADMINS.append(user_id)
    config['DEFAULT']['ADMINS'] = ','.join(ADMINS)
    with open('config.ini', 'w') as file:
        config.write(file)


async def check_if_user_is_admin(user_id: str) -> bool:
    return str(user_id) in ADMINS
