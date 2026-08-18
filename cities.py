from i18n import DEFAULT_LANGUAGE


def get_city_name(city_key, lang):
    data = CITIES[city_key]
    return data["names"].get(lang, data["names"][DEFAULT_LANGUAGE])


CITIES = {
    # Россия
    "yoshkar_ola": {
        "names": {"ru": "Йошкар-Ола", "en": "Yoshkar-Ola", "ja": "ヨシュカル・オラ"},
        "lat": 56.6344,
        "lon": 47.8997,
    },
    "kirov": {
        "names": {"ru": "Киров", "en": "Kirov", "ja": "キーロフ"},
        "lat": 58.6036,
        "lon": 49.6672,
    },
    "moscow": {
        "names": {"ru": "Москва", "en": "Moscow", "ja": "モスクワ"},
        "lat": 55.7558,
        "lon": 37.6173,
    },
    "spb": {
        "names": {"ru": "Санкт-Петербург", "en": "Saint Petersburg", "ja": "サンクトペテルブルク"},
        "lat": 59.9343,
        "lon": 30.3351,
    },
    "novosibirsk": {
        "names": {"ru": "Новосибирск", "en": "Novosibirsk", "ja": "ノヴォシビルスク"},
        "lat": 55.0084,
        "lon": 82.9357,
    },
    "ekaterinburg": {
        "names": {"ru": "Екатеринбург", "en": "Yekaterinburg", "ja": "エカテリンブルク"},
        "lat": 56.8389,
        "lon": 60.6057,
    },
    "kazan": {
        "names": {"ru": "Казань", "en": "Kazan", "ja": "カザン"},
        "lat": 55.7963,
        "lon": 49.1088,
    },
    "nizhny_novgorod": {
        "names": {"ru": "Нижний Новгород", "en": "Nizhny Novgorod", "ja": "ニジニ・ノヴゴロド"},
        "lat": 56.2965,
        "lon": 43.9361,
    },
    "cheboksary": {
        "names": {"ru": "Чебоксары", "en": "Cheboksary", "ja": "チェボクサル"},
        "lat": 56.1465,
        "lon": 47.2516,
    },
    "samara": {
        "names": {"ru": "Самара", "en": "Samara", "ja": "サマラ"},
        "lat": 53.1959,
        "lon": 50.1002,
    },
    "ufa": {
        "names": {"ru": "Уфа", "en": "Ufa", "ja": "ウファ"},
        "lat": 54.7388,
        "lon": 55.9721,
    },
    "perm": {
        "names": {"ru": "Пермь", "en": "Perm", "ja": "ペルミ"},
        "lat": 58.0105,
        "lon": 56.2502,
    },
    "rostov_na_donu": {
        "names": {"ru": "Ростов-на-Дону", "en": "Rostov-on-Don", "ja": "ロストフ・ナ・ドヌ"},
        "lat": 47.2357,
        "lon": 39.7015,
    },
    "volgograd": {
        "names": {"ru": "Волгоград", "en": "Volgograd", "ja": "ヴォルゴグラード"},
        "lat": 48.7071,
        "lon": 44.5169,
    },
    "voronezh": {
        "names": {"ru": "Воронеж", "en": "Voronezh", "ja": "ヴォロネジ"},
        "lat": 51.6606,
        "lon": 39.2003,
    },
    "krasnoyarsk": {
        "names": {"ru": "Красноярск", "en": "Krasnoyarsk", "ja": "クラスノヤルスク"},
        "lat": 56.0153,
        "lon": 92.8932,
    },
    "omsk": {
        "names": {"ru": "Омск", "en": "Omsk", "ja": "オムスク"},
        "lat": 54.9885,
        "lon": 73.3242,
    },
    "tyumen": {
        "names": {"ru": "Тюмень", "en": "Tyumen", "ja": "チュメニ"},
        "lat": 57.1522,
        "lon": 65.5272,
    },
    "vladivostok": {
        "names": {"ru": "Владивосток", "en": "Vladivostok", "ja": "ウラジオストク"},
        "lat": 43.1155,
        "lon": 131.8855,
    },
    "irkutsk": {
        "names": {"ru": "Иркутск", "en": "Irkutsk", "ja": "イルクーツク"},
        "lat": 52.2896,
        "lon": 104.2800,
    },
    "krasnodar": {
        "names": {"ru": "Краснодар", "en": "Krasnodar", "ja": "クラスノダール"},
        "lat": 45.0393,
        "lon": 38.9871,
    },
    "sochi": {
        "names": {"ru": "Сочи", "en": "Sochi", "ja": "ソチ"},
        "lat": 43.6028,
        "lon": 39.7342,
    },
    "kaliningrad": {
        "names": {"ru": "Калининград", "en": "Kaliningrad", "ja": "カリーニングラード"},
        "lat": 54.7104,
        "lon": 20.4522,
    },
    # Мир
    "london": {
        "names": {"ru": "Лондон", "en": "London", "ja": "ロンドン"},
        "lat": 51.5074,
        "lon": -0.1278,
    },
    "paris": {
        "names": {"ru": "Париж", "en": "Paris", "ja": "パリ"},
        "lat": 48.8566,
        "lon": 2.3522,
    },
    "berlin": {
        "names": {"ru": "Берлин", "en": "Berlin", "ja": "ベルリン"},
        "lat": 52.5200,
        "lon": 13.4050,
    },
    "new_york": {
        "names": {"ru": "Нью-Йорк", "en": "New York", "ja": "ニューヨーク"},
        "lat": 40.7128,
        "lon": -74.0060,
    },
    "beijing": {
        "names": {"ru": "Пекин", "en": "Beijing", "ja": "北京"},
        "lat": 39.9042,
        "lon": 116.4074,
    },
    "rome": {
        "names": {"ru": "Рим", "en": "Rome", "ja": "ローマ"},
        "lat": 41.9028,
        "lon": 12.4964,
    },
    "madrid": {
        "names": {"ru": "Мадрид", "en": "Madrid", "ja": "マドリード"},
        "lat": 40.4168,
        "lon": -3.7038,
    },
    "istanbul": {
        "names": {"ru": "Стамбул", "en": "Istanbul", "ja": "イスタンブール"},
        "lat": 41.0082,
        "lon": 28.9784,
    },
    "dubai": {
        "names": {"ru": "Дубай", "en": "Dubai", "ja": "ドバイ"},
        "lat": 25.2048,
        "lon": 55.2708,
    },
    "seoul": {
        "names": {"ru": "Сеул", "en": "Seoul", "ja": "ソウル"},
        "lat": 37.5665,
        "lon": 126.9780,
    },
    "minsk": {
        "names": {"ru": "Минск", "en": "Minsk", "ja": "ミンスク"},
        "lat": 53.9006,
        "lon": 27.5590,
    },
    # Япония
    "tokyo": {
        "names": {"ru": "Токио", "en": "Tokyo", "ja": "東京"},
        "lat": 35.6762,
        "lon": 139.6503,
    },
    "osaka": {
        "names": {"ru": "Осака", "en": "Osaka", "ja": "大阪"},
        "lat": 34.6937,
        "lon": 135.5023,
    },
    "kyoto": {
        "names": {"ru": "Киото", "en": "Kyoto", "ja": "京都"},
        "lat": 35.0116,
        "lon": 135.7681,
    },
    "nagoya": {
        "names": {"ru": "Нагоя", "en": "Nagoya", "ja": "名古屋"},
        "lat": 35.1815,
        "lon": 136.9066,
    },
    "fukuoka": {
        "names": {"ru": "Фукуока", "en": "Fukuoka", "ja": "福岡"},
        "lat": 33.5904,
        "lon": 130.4017,
    },
    "sapporo": {
        "names": {"ru": "Саппоро", "en": "Sapporo", "ja": "札幌"},
        "lat": 43.0618,
        "lon": 141.3545,
    },
    "yokohama": {
        "names": {"ru": "Иокогама", "en": "Yokohama", "ja": "横浜"},
        "lat": 35.4437,
        "lon": 139.6380,
    },
    "kobe": {
        "names": {"ru": "Кобе", "en": "Kobe", "ja": "神戸"},
        "lat": 34.6901,
        "lon": 135.1955,
    },
    "hiroshima": {
        "names": {"ru": "Хиросима", "en": "Hiroshima", "ja": "広島"},
        "lat": 34.3853,
        "lon": 132.4553,
    },
    "sendai": {
        "names": {"ru": "Сендай", "en": "Sendai", "ja": "仙台"},
        "lat": 38.2682,
        "lon": 140.8694,
    },
    "naha": {
        "names": {"ru": "Наха", "en": "Naha", "ja": "那覇"},
        "lat": 26.2124,
        "lon": 127.6809,
    },
    "nagano": {
        "names": {"ru": "Нагано", "en": "Nagano", "ja": "長野"},
        "lat": 36.2380,
        "lon": 138.3630,
    },
}
