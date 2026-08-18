SUPPORTED_LANGUAGES = {"ru", "en", "ja"}
DEFAULT_LANGUAGE = "ru"

LANGUAGE_ALIASES = {"jp": "ja", "jpn": "ja"}


def normalize_language(code):
    if not code:
        return DEFAULT_LANGUAGE
    code = str(code).split("-")[0].strip().lower()
    code = LANGUAGE_ALIASES.get(code, code)
    return code if code in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


TRANSLATIONS = {
    "ru": {
        "greeting": "Привет! Выберите город или отправьте свою локацию:",
        "choose_city": "Выберите город или отправьте свою локацию:",
        "gps_button": "📍 Моя локация (GPS)",
        "back_button": "⬅️ Назад к выбору",
        "location_button": "Отправить местоположение 📍",
        "location_prompt": "Нажми на кнопку внизу экрана 👇",
        "loading": "Загружаю погоду...",
        "weather_template": "🌡 В {city}:\nТемпература: {temp}°C\nНа улице: {condition}",
        "weather_error": "Упс, метеослужба временно не отвечает 😵‍💫",
        "your_location": "вашем месте",
        "unknown_text": "Я тебя не совсем понял, {name}. 😅\nЯ умею показывать погоду. Просто выбери город в меню ниже:",
        "other_types": "Ух ты, красиво! Но я всего лишь погодный бот. Воспользуйся меню: 👇",
        "page_indicator": "стр. {page}/{total}",
    },
    "en": {
        "greeting": "Hi! Choose a city or send your location:",
        "choose_city": "Choose a city or send your location:",
        "gps_button": "📍 My location (GPS)",
        "back_button": "⬅️ Back to cities",
        "location_button": "Send location 📍",
        "location_prompt": "Tap the button at the bottom of the screen 👇",
        "loading": "Loading weather...",
        "weather_template": "🌡 In {city}:\nTemperature: {temp}°C\nConditions: {condition}",
        "weather_error": "Oops, the weather service is temporarily unavailable 😵‍💫",
        "your_location": "your location",
        "unknown_text": "I didn't quite get that, {name}. 😅\nI can show the weather. Just pick a city from the menu below:",
        "other_types": "Wow, nice! But I'm just a weather bot. Use the menu below: 👇",
        "page_indicator": "page {page}/{total}",
    },
    "ja": {
        "greeting": "こんにちは！都市を選ぶか、位置情報を送ってください：",
        "choose_city": "都市を選ぶか、位置情報を送ってください：",
        "gps_button": "📍 現在地 (GPS)",
        "back_button": "⬅️ 都市の選択に戻る",
        "location_button": "現在地を送信 📍",
        "location_prompt": "画面下部のボタンを押してください 👇",
        "loading": "天気を読み込み中...",
        "weather_template": "🌡 {city}の天気:\n気温: {temp}°C\n天候: {condition}",
        "weather_error": "すみません、天気サービスが一時的に利用できません 😵‍💫",
        "your_location": "現在地",
        "unknown_text": "{name}さん、よくわかりませんでした。😅\n天気をお知らせできます。下のメニューから都市を選んでください：",
        "other_types": "わあ、きれい！でも私は天気ボットです。メニューを使ってください：👇",
        "page_indicator": "{page}/{total}ページ",
    },
}

CONDITIONS = {
    "ru": [
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
    ],
    "en": [
        (200, 232, 'Thunderstorm ⚡️'),
        (300, 321, 'Drizzle 🌧'),
        (500, 504, 'Rain 🌧'),
        (511, 511, 'Rain and snow 🌨'),
        (520, 531, 'Downpour 🌧'),
        (600, 622, 'Snow ❄️'),
        (701, 781, 'Fog/mist 🌫'),
        (800, 800, 'Clear ☀️'),
        (801, 801, 'Few clouds 🌤'),
        (802, 802, 'Cloudy ⛅️'),
        (803, 804, 'Overcast ☁️'),
    ],
    "ja": [
        (200, 232, '雷雨 ⚡️'),
        (300, 321, '霧雨 🌧'),
        (500, 504, '雨 🌧'),
        (511, 511, 'みぞれ 🌨'),
        (520, 531, '大雨 🌧'),
        (600, 622, '雪 ❄️'),
        (701, 781, '霧 🌫'),
        (800, 800, '晴れ ☀️'),
        (801, 801, '薄曇り 🌤'),
        (802, 802, '曇り ⛅️'),
        (803, 804, '曇天 ☁️'),
    ],
}


def t(lang, key, **kwargs):
    translations = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE])
    template = translations.get(key, key)
    if kwargs:
        return template.format(**kwargs)
    return template


def get_conditions(lang):
    return CONDITIONS.get(lang, CONDITIONS[DEFAULT_LANGUAGE])
