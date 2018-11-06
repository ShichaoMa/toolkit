from toolkit import test_prepare
test_prepare()
from toolkit.settings import SettingsWrapper


def test_settings():
    sw = SettingsWrapper()
    set = sw.load({"a": 1, "b": "d", "c": {"d": [3,4,5,6], "e": {"a", 4, 5, 6}}})
    print(set)
    print(set.c.e)


if __name__ == "__main__":
    test_settings()