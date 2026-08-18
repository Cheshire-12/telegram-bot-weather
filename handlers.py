from telebot import types
from config import bot
from cities import CITIES
from weather import get_weather
from keyboards import get_cities_keyboard, start_menu_edit


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