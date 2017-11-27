from ..toolkit.settings import SettingsWrapper
import settings
import json


def test_settings():
    sw = SettingsWrapper()
    set = sw.load(default=settings)
    print(json.dumps(set, indent=1))
    print(set.get_float("SPEED"))


if __name__ == "__main__":
    test_settings()