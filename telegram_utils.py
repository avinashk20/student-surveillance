from telegram import Bot
from telegram.utils.request import Request

from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

request = Request(con_pool_size=8, connect_timeout=60)

bot = Bot(token=bot_token, request=request)

def send_alert(caption, photo): 
    try:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
        )
        print('Alert sent')
    except Exception as e:
        print(f"Error sending alert: {e}")

