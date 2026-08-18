from cities import CITIES


def test_every_city_has_fields():
    for key, data in CITIES.items():
        assert "name" in data, key
        assert "lat" in data, key
        assert "lon" in data, key
        assert isinstance(data["name"], str)
        assert isinstance(data["lat"], (int, float))
        assert isinstance(data["lon"], (int, float))


def test_city_coords_in_valid_ranges():
    for key, data in CITIES.items():
        assert -90 <= data["lat"] <= 90, key
        assert -180 <= data["lon"] <= 180, key