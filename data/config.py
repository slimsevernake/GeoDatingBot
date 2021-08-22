from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
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
