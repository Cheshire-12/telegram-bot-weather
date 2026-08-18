import os
import telebot
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not OPENWEATHER_API_KEY:
    print(f"Ошибка: OPENWEATHER_API_KEY не установлен.")
else:
    print(f"OPENWEATHER_API_KEY успешно загружен.")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)