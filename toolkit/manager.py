import warnings
warnings.warn("manager module is a deprecated alias, use managers instead.", DeprecationWarning, 2)
from .managers import Blocker, ExceptContext, Timer

SleepManger = Blocker

__all__ = ["Blocker", "ExceptContext", "Timer", "SleepManger"]
