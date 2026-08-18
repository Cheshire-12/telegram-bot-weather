from telebot import types
from config import bot
from cities import CITIES, get_city_name
from weather import get_weather
from keyboards import get_cities_keyboard, start_menu_edit, _total_pages
from i18n import normalize_language, t


PAGE_STATE = {}


def _get_lang(user):
    return normalize_language(getattr(user, "language_code", None))


def _get_page(chat_id):
    return PAGE_STATE.get(chat_id, 0)


def _set_page(chat_id, page):
    PAGE_STATE[chat_id] = max(0, min(page, _total_pages() - 1))


# Команда /start - Главное меню
@bot.message_handler(commands=['start'])
def start_menu(message):
    lang = _get_lang(message.from_user)
    bot.send_message(message.chat.id, t(lang, "greeting"), reply_markup=get_cities_keyboard(lang))


# Обработка нажатий Inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    lang = _get_lang(call.from_user)
    chat_id = call.message.chat.id

    if call.data.startswith("city_"):
        city_key = call.data.replace("city_", "")
        city_data = CITIES.get(city_key)
        user_first_name = call.from_user.first_name
        user_last_name = call.from_user.last_name or ""
        id = call.from_user.id

        if city_data:
            bot.answer_callback_query(call.id, text=t(lang, "loading"))
            city_name = get_city_name(city_key, lang)
            print(f"Пользователь {user_first_name} {user_last_name}, id: {id}, выбрал {city_data['names']['ru']}")
            text = get_weather(city_data['lat'], city_data['lon'], city_name, lang)

            # Кнопка назад
            back = types.InlineKeyboardMarkup()
            back.add(types.InlineKeyboardButton(t(lang, "back_button"), callback_data="go_back"))

            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back)

    elif call.data == "page_next":
        _set_page(chat_id, _get_page(chat_id) + 1)
        bot.edit_message_text(t(lang, "choose_city"), call.message.chat.id, call.message.message_id,
                              reply_markup=get_cities_keyboard(lang, _get_page(chat_id)))

    elif call.data == "page_prev":
        _set_page(chat_id, _get_page(chat_id) - 1)
        bot.edit_message_text(t(lang, "choose_city"), call.message.chat.id, call.message.message_id,
                              reply_markup=get_cities_keyboard(lang, _get_page(chat_id)))

    elif call.data == "ask_location":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(t(lang, "location_button"), request_location=True))
        bot.send_message(call.message.chat.id, t(lang, "location_prompt"), reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == "go_back":
        # Возвращаем меню (на ту же страницу)
        start_menu_edit(call.message, lang)


# Обработка полученной геолокации
@bot.message_handler(content_types=['location'])
def handle_location(message):
    lang = _get_lang(message.from_user)
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name or ""
    loc_lat = message.location.latitude
    loc_long = message.location.longitude
    res = get_weather(message.location.latitude, message.location.longitude, t(lang, "your_location"), lang)
    print(f"Пользователь {user_first_name} {user_last_name} находится {loc_lat}, {loc_long}")
    bot.send_message(message.chat.id, res, reply_markup=types.ReplyKeyboardRemove())


# Обработка неизвестных сообщений
@bot.message_handler(content_types=['text'])
def echo_all(message):
    lang = _get_lang(message.from_user)
    user_name = message.from_user.first_name
    print(f"---UNKNOWN INPUT---\nПользователь {user_name} ввел: {message.text}")
    bot.reply_to(message, t(lang, "unknown_text", name=user_name),
                 reply_markup=get_cities_keyboard(lang))


@bot.message_handler(content_types=['sticker', 'photo', 'audio', 'video'])
def handle_other_types(message):
    lang = _get_lang(message.from_user)
    bot.send_message(message.chat.id, t(lang, "other_types"), reply_markup=get_cities_keyboard(lang))
