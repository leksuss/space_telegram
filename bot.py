from environs import Env
import telegram


env = Env()
env.read_env()

bot = telegram.Bot(token=env('TG_BOT_API_KEY'))

'''
bot.send_message(
    chat_id=env('TG_CHAT_ID'),
    text="Привет всем! Тут будут просто космические фотки",
)
'''

bot.send_photo(
    chat_id=env('TG_CHAT_ID'),
    photo=open('apod_images/saturnrhea_cassini_960.jpg', 'rb'),
)
