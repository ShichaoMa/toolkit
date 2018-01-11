from toolkit.settings import SettingsWrapper
import json


def test_settings():
    sw = SettingsWrapper()
    set = sw.load(default={"SPEED", 1})
    print(set)
    print(set.get_float("SPEED"))


if __name__ == "__main__":
    test_settings()