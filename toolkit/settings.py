"""
settings模块使用方法
In [3]: from toolkit.settings import SettingsLoader

In [4]: sw = SettingsLoader()

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
import copy
import types
import logging
import importlib

from numbers import Number
from collections import UserDict
from collections.abc import Collection, MutableSequence, MutableSet, MutableMapping

from . import duplicate
from .frozen import FrozenSettings

__all__ = ["Settings", "SettingsLoader", "FrozenSettings"]

logger = logging.getLogger("toolkit.settings")


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


class SettingsLoader(object):
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
    allow_types = [Collection, Number]

    def __init__(self, settings_type=Settings):
        self.settings = settings_type()

    @classmethod
    def register_types(cls, types):
        cls.allow_types.extend(types)

    def load(self, local='localsettings', default='settings'):
        """
        加载配置字典
        :param local: 本地配置模块
        :param default: 默认配置模块
        :return: 配置信息字典
        """
        for settings in [default, local]:
            if isinstance(settings, MutableMapping):
                self.merge(self.settings, settings)
            else:
                self._load(settings)

        return FrozenSettings(self.settings)

    def load_from_string(self, settings_string='', module_name='customsettings'):
        """
        从配置语句中获取配置信息
        :param settings_string: 配置信息语句
        :param module_name: 配置信息的环境变量
        :return:
        """
        try:
            mod = types.ModuleType(module_name)
            exec(settings_string, mod.__dict__)
        except TypeError:
            logger.warning("Could not import settings from string.")
            mod = None
        try:
            self.merge(self.settings, self._convert_to_dict(mod))
        except ImportError:
            logger.warning("Settings from string unable to be loaded.")

    def _load(self, setting_module):
        try:
            if isinstance(setting_module, str):
                if setting_module[-3:] == '.py':
                    setting_module = setting_module[:-3].replace(
                        os.sep, ".").strip(".")
                settings = importlib.import_module(setting_module)
            else:
                settings = setting_module
            self.merge(self.settings, self._convert_to_dict(settings))
        except ImportError:
            logger.warning("Cannot found %s." % setting_module)

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
                    for v in new_value:
                        value.add(v)
                elif isinstance(value, MutableSequence):
                    value.extend(new_value)
                    settings[key] = duplicate(value, reverse=True)
                else:
                    settings[key] = new_value
            else:
                settings[key] = new_value

    def _convert_to_dict(self, settings):
        """
        将配置文件转化为字典
        :param setting:
        :return:
        """
        allow_types = tuple(self.allow_types)
        return dict(
            (k, copy.deepcopy(getattr(settings, k))) for k in dir(settings)
            if k not in self.ignore and isinstance(
                getattr(settings, k), allow_types))
