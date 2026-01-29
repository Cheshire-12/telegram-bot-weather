import os
import telebot
import requests
import time
import functools
from telebot import types
from dotenv import load_dotenv
from cities import CITIES

load_dotenv()
YANDEX_WEATHER_API_KEY = os.getenv("YANDEX_WEATHER_API_KEY")
API_TOKEN = os.getenv("API_KEY")
if not YANDEX_WEATHER_API_KEY:
    print(f"Ошибка: YANDEX_WEATHER_API_KEY не установлен.")
else:
    print(f"YANDEX_WEATHER_API_KEY успешно загружен.")
bot = telebot.TeleBot(API_TOKEN)

# Декоратор для замера времени выполнения функции
def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        stop_time = time.time()
        execution_time = stop_time - start_time
        print(f'Функция {func.__name__} выполнена за {round(execution_time, 3)} секунд')
        return result
    return wrapper

# Яндкес погода
WEATHER_CONDITIONS = {
    'clear': 'Ясно ☀️', 'partly-cloudy': 'Малооблачно 🌤', 'cloudy': 'Облачно ⛅️',
    'overcast': 'Пасмурно ☁️', 'drizzle': 'Морось 🌧', 'light-rain': 'Небольшой дождь 🌦',
    'rain': 'Дождь 🌧', 'moderate-rain': 'Сильный дождь ⛈', 'heavy-rain': 'Ливень 🌊',
    'snow': 'Снег ❄️',"light-snow": "Легкий снег ❄️","snowfall": "Снегопад",'thunderstorm': 'Гроза ⚡️'
}

# Функция для получения погоды
@log_function_call
def get_weather(lat, lon, city_name="выбранном месте"):
    url = "https://api.weather.yandex.ru/v2/forecast"
    headers = {"X-Yandex-Weather-Key": YANDEX_WEATHER_API_KEY}
    params = {"lat": lat, "lon": lon, "lang": "ru_RU"}
    print(f"Используется API key: {YANDEX_WEATHER_API_KEY[0:4]}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        temp = data['fact']['temp']
        cond_key = data['fact']['condition']
        condition = WEATHER_CONDITIONS.get(cond_key, cond_key.replace('-', ' '))
        print(f"Temp - {temp}, condition - {cond_key}")
        return f"🌡 В {city_name}:\nТемпература: {temp}°C\nНа улице: {condition}"
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Упс, метеослужба временно не отвечает 😵‍💫"
    

# Функция для создания клавиатуры с городами
def get_cities_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(data['name'], callback_data=f"city_{key}") 
            for key, data in CITIES.items()]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("📍 Моя локация (GPS)", callback_data="ask_location"))
    return markup

    
# Команда /start - Главное меню
@bot.message_handler(commands=['start'])
def start_menu(message):
    bot.send_message(message.chat.id, "Привет! Выберите город или отправьте свою локацию:", reply_markup=get_cities_keyboard())

# Обработка нажатий Inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith("city_"):
        city_key = call.data.replace("city_", "")
        city_data = CITIES.get(city_key)
        user_first_name = call.from_user.first_name
        user_last_name = call.from_user.last_name or ""
        id = call.from_user.id
        
        if city_data:
            bot.answer_callback_query(call.id, text="Загружаю погоду...")
            print(f"Пользователь {user_first_name} {user_last_name}, id: {id}, выбрал {city_data['name']}")
            text = get_weather(city_data['lat'], city_data['lon'], city_data['name'])
            
            # Кнопка назад
            back = types.InlineKeyboardMarkup()
            back.add(types.InlineKeyboardButton("⬅️ Назад к выбору", callback_data="go_back"))
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back)

    elif call.data == "ask_location":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Отправить местоположение 📍", request_location=True))
        bot.send_message(call.message.chat.id, "Нажми на кнопку внизу экрана 👇", reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == "go_back":
        # Возвращаем меню (просто вызываем функцию заново, но с edit)
        start_menu_edit(call.message)

def start_menu_edit(message):
    bot.edit_message_text("Выберите город или отправьте свою локацию:", message.chat.id, message.message_id, reply_markup=get_cities_keyboard())

# Обработка полученной геолокации
@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name or ""
    loc_lat = message.location.latitude
    loc_long = message.location.longitude
    res = get_weather(message.location.latitude, message.location.longitude, "вашем месте")
    print(f"Пользователь {user_first_name} {user_last_name} находится {loc_lat}, {loc_long}")
    bot.send_message(message.chat.id, res, reply_markup=types.ReplyKeyboardRemove())

# Обработка неизвестных сообщений
@bot.message_handler(content_types=['text'])
def echo_all(message):
    user_name = message.from_user.first_name
    print(f"---UNKNOWN INPUT---\nПользователь {user_name} ввел: {message.text}")
    bot.reply_to(message, 
                 f"Я тебя не совсем понял, {user_name}. 😅\n"
                 "Я умею показывать погоду. Просто выбери город в меню ниже:", 
                 reply_markup=get_cities_keyboard())
    
@bot.message_handler(content_types=['sticker', 'photo', 'audio', 'video'])
def handle_other_types(message):
    bot.send_message(message.chat.id, "Ух ты, красиво! Но я всего лишь погодный бот. Воспользуйся меню: 👇", 
                     reply_markup=get_cities_keyboard())

# Запуск бота
print("Бот запущен и готов к работе...")
bot.infinity_polling()