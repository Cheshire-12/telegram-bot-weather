from cities import CITIES, get_city_name
from i18n import SUPPORTED_LANGUAGES


def test_every_city_has_fields():
    for key, data in CITIES.items():
        assert "names" in data, key
        assert "lat" in data, key
        assert "lon" in data, key
        assert isinstance(data["names"], dict)
        assert isinstance(data["lat"], (int, float))
        assert isinstance(data["lon"], (int, float))


def test_every_city_has_all_languages():
    for key, data in CITIES.items():
        for lang in SUPPORTED_LANGUAGES:
            assert lang in data["names"], (key, lang)
            assert isinstance(data["names"][lang], str)
            assert data["names"][lang].strip(), (key, lang)


def test_city_coords_in_valid_ranges():
    for key, data in CITIES.items():
        assert -90 <= data["lat"] <= 90, key
        assert -180 <= data["lon"] <= 180, key


def test_get_city_name_returns_localized():
    assert get_city_name("moscow", "ru") == "Москва"
    assert get_city_name("moscow", "en") == "Moscow"
    assert get_city_name("moscow", "ja") == "モスクワ"
    assert get_city_name("tokyo", "ja") == "東京"


def test_get_city_name_falls_back_to_default():
    assert get_city_name("moscow", "fr") == "Москва"
