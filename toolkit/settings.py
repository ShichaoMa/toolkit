import os
import types
import importlib

from . import duplicate


class Settings(dict):
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
        except ValueError:
            return d

    def get_bool(self, k, d=False):
        try:
            try:
                return eval(self.get(k, str(d)))
            except:
                pass
            return bool(self.get(k, d))
        except ValueError:
            return d

    def get_float(self, k, d=None):
        try:
            return float(self.get(k, d))
        except ValueError:
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

    def __init__(self):
        self.my_settings = Settings()

    def load(self, local='localsettings', default='settings'):
        """
        加载配置字典
        :param local: 本地配置模块
        :param default: 默认配置模块
        :return: 配置信息字典
        """
        self._load_defaults(default)
        self._load_custom(local)

        return self.my_settings

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
            self.my_settings.update(self._convert_to_dict(mod))
        except ImportError:
            print("Settings unable to be loaded")

        return self.my_settings

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
            self.my_settings.update(self._convert_to_dict(settings))
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
        self.merge(self.my_settings, new_settings)

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
                if isinstance(value, dict):
                    self.merge(value, new_value)
                elif isinstance(value, set):
                    value.update(new_value)
                elif isinstance(value, list):
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
            if isinstance(value, (bytes, str, list, set, dict, int, float, bool)):
                the_dict[key] = value
        return the_dict


