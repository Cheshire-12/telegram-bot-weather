import time
import functools
import requests
from config import OPENWEATHER_API_KEY


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


# Диапазоны кодов условий OpenWeatherMap: (from_id, to_id, описание)
OWM_CONDITIONS = [
    (200, 232, 'Гроза ⚡️'),
    (300, 321, 'Морось 🌧'),
    (500, 504, 'Дождь 🌧'),
    (511, 511, 'Дождь со снегом 🌨'),
    (520, 531, 'Ливень 🌧'),
    (600, 622, 'Снег ❄️'),
    (701, 781, 'Туман/мгла 🌫'),
    (800, 800, 'Ясно ☀️'),
    (801, 801, 'Малооблачно 🌤'),
    (802, 802, 'Облачно ⛅️'),
    (803, 804, 'Пасмурно ☁️'),
]


def owm_condition(weather_id):
    for lo, hi, text in OWM_CONDITIONS:
        if lo <= weather_id <= hi:
            return text
    return None


# Функция для получения погоды
@log_function_call
def get_weather(lat, lon, city_name="выбранном месте"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        temp = round(data['main']['temp'])
        weather_id = data['weather'][0]['id']
        condition = owm_condition(weather_id) or data['weather'][0]['description']
        print(f"Temp - {temp}, condition_id - {weather_id}")
        return f"🌡 В {city_name}:\nТемпература: {temp}°C\nНа улице: {condition}"

    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        print(f"Ошибка: сервер погоды вернул статус {status}")
        return "Упс, метеослужба временно не отвечает 😵‍💫"
    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}")
        return "Упс, метеослужба временно не отвечает 😵‍💫"