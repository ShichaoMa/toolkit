import sys
import time
from argparse import ArgumentParser
sys.path.insert(0, "/Users/mashichao/myprojects/toolkit")
from toolkit.consoler import Consoler
from toolkit.monitors import ParallelMonitor


class Service(Consoler, ParallelMonitor):

    args = None

    def __init__(self):
        self.args = self.parse_args()
        super(Service, self).__init__(locals())

    def start(self):
        while self.alive:
            time.sleep(1)

    def parse_args(self):
        self.parser = ArgumentParser(conflict_handler="resolve")
        self.enrich_parser_arguments()
        return self.parser.parse_args()


Service().start()