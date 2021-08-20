from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
DEBUG = int(env.str('DEBUG'))
if DEBUG:
    REDIS_HOST = 'localhost'
else:
    REDIS_HOST = '188.225.43.69'
