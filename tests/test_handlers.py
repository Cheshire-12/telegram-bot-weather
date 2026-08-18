from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import handlers
import keyboards


def make_message(text=None, chat_id=123, language_code="ru"):
    return SimpleNamespace(
        from_user=SimpleNamespace(first_name="Иван", last_name=None, language_code=language_code),
        chat=SimpleNamespace(id=chat_id),
        text=text,
    )


def make_call(callback_data, message_id=42, chat_id=123, language_code="ru"):
    return SimpleNamespace(
        data=callback_data,
        id="cb123",
        from_user=SimpleNamespace(first_name="Иван", last_name=None, id=1, language_code=language_code),
        message=SimpleNamespace(chat=SimpleNamespace(id=chat_id), message_id=message_id),
    )


def flatten_markup(markup):
    return [btn for row in markup.keyboard for btn in row]


def _has_request_location(btn):
    if isinstance(btn, dict):
        return btn.get("request_location", False)
    return getattr(btn, "request_location", False)


@pytest.fixture
def fake_bot(monkeypatch):
    bot = MagicMock()
    monkeypatch.setattr(handlers, "bot", bot)
    monkeypatch.setattr(keyboards, "bot", bot)
    return bot


def test_city_selection_edits_message(fake_bot, monkeypatch):
    monkeypatch.setattr(handlers, "get_weather", lambda lat, lon, name, lang: f"Погода в {name}")
    fake_bot.answer_callback_query.return_value = None

    handlers.handle_query(make_call("city_kirov"))

    fake_bot.answer_callback_query.assert_called_once()
    fake_bot.edit_message_text.assert_called_once()
    text = fake_bot.edit_message_text.call_args.args[0]
    assert "Погода в Киров" in text


def test_city_selection_localized_name_and_lang(fake_bot, monkeypatch):
    captured = {}
    def fake_weather(lat, lon, name, lang):
        captured["name"] = name
        captured["lang"] = lang
        return f"Погода в {name}"
    monkeypatch.setattr(handlers, "get_weather", fake_weather)
    fake_bot.answer_callback_query.return_value = None

    handlers.handle_query(make_call("city_moscow", language_code="ja"))

    assert captured["name"] == "モスクワ"
    assert captured["lang"] == "ja"


def test_city_selection_unknown_city_does_nothing(fake_bot):
    handlers.handle_query(make_call("city_not_exist"))
    fake_bot.answer_callback_query.assert_not_called()
    fake_bot.edit_message_text.assert_not_called()


def test_ask_location_sends_reply_keyboard(fake_bot):
    handlers.handle_query(make_call("ask_location"))
    kwargs = fake_bot.send_message.call_args.kwargs
    markup = kwargs["reply_markup"]
    buttons = flatten_markup(markup)
    assert any(_has_request_location(b) for b in buttons)


def test_go_back_returns_to_menu(fake_bot):
    handlers.handle_query(make_call("go_back"))
    fake_bot.edit_message_text.assert_called_once()


def test_page_next_advances_page(fake_bot):
    handlers.handle_query(make_call("page_next", chat_id=999))
    fake_bot.edit_message_text.assert_called_once()
    kwargs = fake_bot.edit_message_text.call_args.kwargs
    assert "reply_markup" in kwargs
    assert handlers.PAGE_STATE.get(999) == 1


def test_page_prev_returns_page(fake_bot):
    handlers.PAGE_STATE[999] = 2
    handlers.handle_query(make_call("page_prev", chat_id=999))
    assert handlers.PAGE_STATE.get(999) == 1


def test_page_state_reset_between_chats(fake_bot):
    handlers.PAGE_STATE[100] = 3
    handlers.handle_query(make_call("page_next", chat_id=200))
    assert handlers.PAGE_STATE.get(200) == 1
    assert handlers.PAGE_STATE.get(100) == 3


def test_location_sends_weather(fake_bot, monkeypatch):
    monkeypatch.setattr(handlers, "get_weather", lambda lat, lon, name, lang: "погода в месте")
    message = SimpleNamespace(
        from_user=SimpleNamespace(first_name="Иван", last_name="Петров", language_code="ru"),
        chat=SimpleNamespace(id=123),
        location=SimpleNamespace(latitude=55.7558, longitude=37.6173),
    )
    handlers.handle_location(message)
    fake_bot.send_message.assert_called_once()


def test_unknown_text_replies_with_keyboard(fake_bot):
    handlers.echo_all(make_message("непонятно"))
    fake_bot.reply_to.assert_called_once()


def test_unknown_text_localized(fake_bot):
    handlers.echo_all(make_message("непонятно", language_code="en"))
    text = fake_bot.reply_to.call_args.args[1]
    assert "I didn't quite get that" in text


def test_other_types_send_hint(fake_bot):
    handlers.handle_other_types(make_message())
    fake_bot.send_message.assert_called_once()
