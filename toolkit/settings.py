"""
settings模块使用方法
In [3]: from toolkit.settings import SettingsWrapper

In [4]: sw = SettingsWrapper()

In [5]: settings = sw.load({"a": 1}， "settings")

In [6]: settings
Out[6]: {'AUTHOR': '夏洛之枫', 'DB': 'sqlite', 'a': 1}

In [8]: settings.a
Out[8]: 1

In [9]: settings["a"]
Out[9]: 1

In [10]: settings.get("a")
Out[10]: 1

In [13]: import os

In [15]: os.environ["b"] = "3"

In [16]: settings.get_int("b", 11)
Out[16]: 3

In [18]: settings2 = sw.load({"a": 1, "c": {"d": [3,4,5,6], "e": {"a", 4, 5,6}}})

In [19]: settings2 is settings
Out[19]: False

In [21]: settings2.a
Out[21]: 1

In [22]: settings2.b
Out[22]: '3'

In [23]: settings2.c
Out[23]: {'d': [3, 4, 5, 6], 'e': {4, 5, 6, 'a'}}

In [24]: type(settings2.c)
Out[24]: toolkit.frozen.Frozen

In [26]: settings2.c.e
Out[26]: {4, 5, 6, 'a'}

In [27]: type(settings2.c.e)
Out[27]: set

In [28]: type(settings2.c.d)
Out[28]: toolkit.frozen.Frozen
"""
import os
import types
import importlib

from . import duplicate
from .frozen import Frozen
from collections import UserDict
from collections.abc import MutableMapping, MutableSet, MutableSequence

__all__ = ["Settings", "SettingsWrapper"]


class Settings(UserDict):
    """
    settings，首先从环境变量从获取
    """
    def __getitem__(self, item):
        if item in os.environ:
            return os.environ[item]
        return super(Settings, self).__getitem__(item)

    def get(self, k, d=None):
        if k in os.environ:
            return os.environ[k]
        return super(Settings, self).get(k, d)

    def get_int(self, k, d=None):
        try:
            return int(self.get(k, d))
        except TypeError:
            return d

    def get_bool(self, k, d=False):
        try:
            try:
                return eval(self.get(k, str(d)))
            except:
                pass
            return bool(self.get(k, d))
        except TypeError:
            return d

    def get_float(self, k, d=None):
        try:
            return float(self.get(k, d))
        except TypeError:
            return d


class SettingsWrapper(object):
    """
    配置文件加载装饰器用来加载和覆盖配置信息
    """
    ignore = [
        '__builtins__',
        '__file__',
        '__package__',
        '__doc__',
        '__name__',
        '__cached__',
    ]
    settings = None

    def __init__(self, settings_type=Settings):
        super(SettingsWrapper, self).__init__()
        self.settings_type = settings_type

    def load(self, local='localsettings', default='settings'):
        """
        加载配置字典
        :param local: 本地配置模块
        :param default: 默认配置模块
        :return: 配置信息字典
        """
        self.settings = self.settings_type()
        if isinstance(default, MutableMapping):
            self.merge(self.settings, default)
        else:
            self._load_defaults(default)

        if isinstance(local, MutableMapping):
            self.merge(self.settings, local)
        else:
            self._load_custom(local)
        return Frozen(self.settings)

    def load_from_string(self, settings_string='', module_name='customsettings'):
        """
        从配置语句中获取配置信息
        :param settings_string: 配置信息语句
        :param module_name: 配置信息的环境变量
        :return:
        """
        mod = None
        try:
            mod = types.ModuleType(module_name)
            exec(settings_string in mod.__dict__)
        except TypeError:
            print("Could not import settings")
        try:
            self.settings.update(self._convert_to_dict(mod))
        except ImportError:
            print("Settings unable to be loaded")

    def _load_defaults(self, default='settings'):
        """
        加载默认配置信息
        :param default:
        :return:
        """
        if isinstance(default, str) and default[-3:] == '.py':
            default = default[:-3]
        try:
            if isinstance(default, str):
                settings = importlib.import_module(default)
            else:
                settings = default
            self.settings.update(self._convert_to_dict(settings))
        except ImportError:
            print("No default settings found")

    def _load_custom(self, settings_name='localsettings'):
        """
        加载自定义配置信息，覆盖默认配置
        :param settings_name:
        :return:
        """
        if isinstance(settings_name, str) and settings_name[-3:] == '.py':
            settings_name = settings_name[:-3]

        new_settings = dict()
        try:
            if isinstance(settings_name, str):
                settings = importlib.import_module(settings_name)
            else:
                settings = settings_name
            new_settings.update(self._convert_to_dict(settings))
        except ImportError:
            print("No override settings found")
        self.merge(self.settings, new_settings)

    def merge(self, settings, new_settings):
        """
        合并settings
        :param settings:
        :param new_settings:
        :return:
        """
        for key in new_settings:
            value = settings.get(key)
            new_value = new_settings[key]
            if type(value) == type(new_value):
                if isinstance(value, MutableMapping):
                    self.merge(value, new_value)
                elif isinstance(value, MutableSet):
                    value.update(new_value)
                elif isinstance(value, MutableSequence):
                    value.extend(new_value)
                    settings[key] = duplicate(value, reverse=True)
                else:
                    settings[key] = new_value
            else:
                settings[key] = new_value

    def _convert_to_dict(self, setting):
        """
        将配置文件转化为字典
        :param setting:
        :return:
        """
        the_dict = {}
        for key in dir(setting):
            if key in self.ignore:
                continue
            value = getattr(setting, key)
            if isinstance(value, (bytes, str, MutableSet, MutableSequence, MutableMapping, int, float, bool)):
                the_dict[key] = value
        return the_dict


