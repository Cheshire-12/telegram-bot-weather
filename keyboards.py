from telebot import types
from config import bot
from cities import CITIES


# Функция для создания клавиатуры с городами
def get_cities_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(data['name'], callback_data=f"city_{key}")
            for key, data in CITIES.items()]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("📍 Моя локация (GPS)", callback_data="ask_location"))
    return markup


def start_menu_edit(message):
    bot.edit_message_text("Выберите город или отправьте свою локацию:", message.chat.id, message.message_id, reply_markup=get_cities_keyboard())