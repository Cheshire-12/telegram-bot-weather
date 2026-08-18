import requests
import weather


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def mock_get(monkeypatch, payload):
    monkeypatch.setattr(weather, "OPENWEATHER_API_KEY", "test_key")
    monkeypatch.setattr(weather.requests, "get", lambda url, params: FakeResponse(payload))


def _payload(temp, weather_id, description):
    return {"main": {"temp": temp}, "weather": [{"id": weather_id, "description": description}]}


def test_get_weather_success(monkeypatch):
    mock_get(monkeypatch, _payload(15.2, 800, "ясно"))
    result = weather.get_weather(55.7558, 37.6173, "Москва", "ru")
    assert "Москва" in result
    assert "15" in result
    assert "Ясно" in result


def test_get_weather_snow(monkeypatch):
    mock_get(monkeypatch, _payload(-3.4, 601, "снег"))
    result = weather.get_weather(56.6344, 47.8997, "Йошкар-Ола", "ru")
    assert "Снег" in result


def test_get_weather_overcast(monkeypatch):
    mock_get(monkeypatch, _payload(5.0, 804, "пасмурно"))
    result = weather.get_weather(0, 0, "Тест", "ru")
    assert "Пасмурно" in result


def test_get_weather_english(monkeypatch):
    mock_get(monkeypatch, _payload(15.2, 800, "clear sky"))
    result = weather.get_weather(51.5074, -0.1278, "London", "en")
    assert "London" in result
    assert "Clear" in result


def test_get_weather_japanese(monkeypatch):
    mock_get(monkeypatch, _payload(-3.4, 601, "snow"))
    result = weather.get_weather(35.6762, 139.6503, "東京", "ja")
    assert "東京" in result
    assert "雪" in result


def test_get_weather_passes_lang_to_api(monkeypatch):
    captured = {}
    monkeypatch.setattr(weather, "OPENWEATHER_API_KEY", "test_key")
    monkeypatch.setattr(weather.requests, "get", lambda url, params: (captured.update(params), FakeResponse(_payload(0, 800, "")))[1])
    weather.get_weather(0, 0, "Тест", "ja")
    assert captured["lang"] == "ja"


def test_get_weather_falls_back_to_description(monkeypatch):
    mock_get(monkeypatch, _payload(7.1, 999, "особая погода"))
    result = weather.get_weather(0, 0, "Тест", "ru")
    assert "особая погода" in result


def test_get_weather_request_error(monkeypatch):
    monkeypatch.setattr(weather, "OPENWEATHER_API_KEY", "test_key")

    def boom(url, params):
        raise requests.exceptions.HTTPError("boom")

    monkeypatch.setattr(weather.requests, "get", boom)
    result = weather.get_weather(0, 0, "Тест", "ru")
    assert "метеослужба временно не отвечает" in result


def test_get_weather_error_localized(monkeypatch):
    monkeypatch.setattr(weather, "OPENWEATHER_API_KEY", "test_key")

    def boom(url, params):
        raise requests.exceptions.HTTPError("boom")

    monkeypatch.setattr(weather.requests, "get", boom)
    result = weather.get_weather(0, 0, "Test", "en")
    assert "weather service is temporarily unavailable" in result


def test_get_weather_error_log_does_not_leak_key(monkeypatch, capsys):
    monkeypatch.setattr(weather, "OPENWEATHER_API_KEY", "supersecret-key")

    def boom(url, params):
        raise requests.exceptions.HTTPError(
            "401 Unauthorized for url: https://api.openweathermap.org/data/2.5/weather?appid=supersecret-key"
        )

    monkeypatch.setattr(weather.requests, "get", boom)
    weather.get_weather(0, 0, "Тест", "ru")
    captured = capsys.readouterr().out
    assert "supersecret-key" not in captured
    assert "api.openweathermap.org" not in captured
