from types import SimpleNamespace
from unittest.mock import MagicMock

import keyboards
from cities import CITIES


def _flatten(markup):
    return [btn for row in markup.keyboard for btn in row]


def test_get_cities_keyboard_has_all_cities_plus_gps():
    markup = keyboards.get_cities_keyboard()
    buttons = _flatten(markup)
    callback_datas = {btn.callback_data for btn in buttons}
    assert len(buttons) == len(CITIES) + 1
    for key in CITIES:
        assert f"city_{key}" in callback_datas
    assert "ask_location" in callback_datas


def test_get_cities_keyboard_button_labels():
    markup = keyboards.get_cities_keyboard()
    buttons = _flatten(markup)
    labels = {btn.text for btn in buttons}
    for data in CITIES.values():
        assert data["name"] in labels


def test_start_menu_edit(monkeypatch):
    fake_bot = MagicMock()
    monkeypatch.setattr(keyboards, "bot", fake_bot)
    message = SimpleNamespace(chat=SimpleNamespace(id=1), message_id=10)
    keyboards.start_menu_edit(message)
    fake_bot.edit_message_text.assert_called_once()
    kwargs = fake_bot.edit_message_text.call_args.kwargs
    assert "reply_markup" in kwargs