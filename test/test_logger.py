from toolkit.logger import Logger
from toolkit.settings import SettingsWrapper

from threading import Thread


class A(object):

    def __init__(self):
        self.logger = Logger(SettingsWrapper().load({"a": 1}))


def log_thread():
    A().logger.info("11111111")

for i in range(5):
    Thread(target=log_thread).start()
