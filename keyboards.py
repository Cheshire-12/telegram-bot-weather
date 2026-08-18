from telebot import types
from config import bot
from cities import CITIES, get_city_name
from i18n import t

PAGE_SIZE = 8


def _total_pages():
    total = len(CITIES)
    return max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)


def _page_cities(page):
    items = list(CITIES.items())
    start = page * PAGE_SIZE
    return items[start:start + PAGE_SIZE]


def get_cities_keyboard(lang, page=0):
    total_pages = _total_pages()
    page = max(0, min(page, total_pages - 1))

    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton(get_city_name(key, lang), callback_data=f"city_{key}")
        for key, data in _page_cities(page)
    ]
    markup.add(*btns)

    if total_pages > 1:
        nav_btns = []
        if page > 0:
            nav_btns.append(types.InlineKeyboardButton("◀️", callback_data="page_prev"))
        nav_btns.append(types.InlineKeyboardButton(
            t(lang, "page_indicator", page=page + 1, total=total_pages), callback_data="page_indicator"))
        if page < total_pages - 1:
            nav_btns.append(types.InlineKeyboardButton("▶️", callback_data="page_next"))
        markup.add(*nav_btns)

    markup.add(types.InlineKeyboardButton(t(lang, "gps_button"), callback_data="ask_location"))
    return markup


def start_menu_edit(message, lang):
    bot.edit_message_text(t(lang, "choose_city"), message.chat.id, message.message_id,
                          reply_markup=get_cities_keyboard(lang))
