from toolkit.settings import SettingsLoader


def test_settings():
    sw = SettingsLoader()
    set = sw.load({"a": 1, "b": "d", "c": {"d": [3,4,5,6], "e": {"a", 4, 5, 6}}})
    print(set)
    print(set.c.e)
