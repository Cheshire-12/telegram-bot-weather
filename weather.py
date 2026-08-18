import time
import functools
import requests
from config import OPENWEATHER_API_KEY
from i18n import get_conditions, t, DEFAULT_LANGUAGE


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


def owm_condition(weather_id, lang=DEFAULT_LANGUAGE):
    for lo, hi, text in get_conditions(lang):
        if lo <= weather_id <= hi:
            return text
    return None


# Функция для получения погоды
@log_function_call
def get_weather(lat, lon, city_name="выбранном месте", lang=DEFAULT_LANGUAGE):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": lang,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        temp = round(data['main']['temp'])
        weather_id = data['weather'][0]['id']
        condition = owm_condition(weather_id, lang) or data['weather'][0]['description']
        print(f"Temp - {temp}, condition_id - {weather_id}")
        return t(lang, "weather_template", city=city_name, temp=temp, condition=condition)

    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        print(f"Ошибка: сервер погоды вернул статус {status}")
        return t(lang, "weather_error")
    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}")
        return t(lang, "weather_error")
