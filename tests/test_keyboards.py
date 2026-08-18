from types import SimpleNamespace
from unittest.mock import MagicMock

import keyboards
from cities import CITIES, get_city_name
from keyboards import PAGE_SIZE, _total_pages


def _flatten(markup):
    return [btn for row in markup.keyboard for btn in row]


def _buttons(markup):
    return _flatten(markup)


def test_keyboard_has_only_one_page_of_cities():
    markup = keyboards.get_cities_keyboard("ru")
    buttons = _buttons(markup)
    callback_datas = {btn.callback_data for btn in buttons}
    city_buttons = [cb for cb in callback_datas if cb.startswith("city_")]
    assert len(city_buttons) <= PAGE_SIZE
    assert "ask_location" in callback_datas


def test_keyboard_first_page_has_next_and_no_prev():
    markup = keyboards.get_cities_keyboard("ru", page=0)
    callback_datas = {btn.callback_data for btn in _buttons(markup)}
    assert "page_next" in callback_datas
    assert "page_prev" not in callback_datas
    assert "page_indicator" in callback_datas


def test_keyboard_last_page_has_prev_and_no_next():
    last_page = _total_pages() - 1
    markup = keyboards.get_cities_keyboard("ru", page=last_page)
    callback_datas = {btn.callback_data for btn in _buttons(markup)}
    assert "page_prev" in callback_datas
    assert "page_next" not in callback_datas


def test_all_cities_covered_across_pages():
    seen = set()
    total_pages = _total_pages()
    for page in range(total_pages):
        markup = keyboards.get_cities_keyboard("ru", page=page)
        for btn in _buttons(markup):
            if btn.callback_data.startswith("city_"):
                seen.add(btn.callback_data.replace("city_", ""))
    assert seen == set(CITIES.keys())


def test_keyboard_button_labels_localized():
    markup = keyboards.get_cities_keyboard("ja")
    labels = {btn.text for btn in _buttons(markup)}
    city_keys = [cb.replace("city_", "") for cb in (btn.callback_data for btn in _buttons(markup)) if cb.startswith("city_")]
    for key in city_keys:
        assert get_city_name(key, "ja") in labels


def test_page_indicator_shows_current_and_total():
    markup = keyboards.get_cities_keyboard("en", page=1)
    labels = {btn.text for btn in _buttons(markup)}
    assert f"page 2/{_total_pages()}" in labels


def test_start_menu_edit(monkeypatch):
    fake_bot = MagicMock()
    monkeypatch.setattr(keyboards, "bot", fake_bot)
    message = SimpleNamespace(chat=SimpleNamespace(id=1), message_id=10)
    keyboards.start_menu_edit(message, "ru")
    fake_bot.edit_message_text.assert_called_once()
    kwargs = fake_bot.edit_message_text.call_args.kwargs
    assert "reply_markup" in kwargs
