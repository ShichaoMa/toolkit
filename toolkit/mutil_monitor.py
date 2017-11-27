import os
import sys
import signal
import logging


class MultiMonitor(object):

    alive = True
    name = "root"
    children = []
    int_signal_count = 1

    def __init__(self):
        self.open()

    def set_logger(self, logger=None):
        if not logger:
            self.logger = logging.getLogger(self.name)
            self.logger.setLevel(10)
            self.logger.addHandler(logging.StreamHandler(sys.stdout))
        else:
            self.logger = logger
            self.name = logger.name

    def stop(self, *args):
        if self.int_signal_count > 1:
            self.logger.info("force to terminate...")
            for th in self.children[:]:
                self.stop_child(th)
            pid = os.getpid()
            os.kill(pid, 9)

        else:
            self.alive = False
            self.logger.info("close process %s..." % self.name)
            self.int_signal_count += 1

    def open(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop_child(self, child):
        pass
