from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
DB_NAME = env.str('DB_NAME')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_USER = env.str('DB_USER')
DEBUG = int(env.str('DEBUG'))
if DEBUG:
    REDIS_HOST = 'localhost'
else:
    REDIS_HOST = '188.225.43.69'
