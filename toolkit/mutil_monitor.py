import warnings
warnings.warn("mutil_monitor module is a deprecated alias, use monitors instead. ", DeprecationWarning, 2)
from .monitors import ParallelMonitor as MultiMonitor

__all__ = ["MultiMonitor"]
