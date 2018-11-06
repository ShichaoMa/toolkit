import time
from toolkit import test_prepare
test_prepare()
from argparse import ArgumentParser
from toolkit.consoler import Consoler


class Service(Consoler):

    args = None

    def __init__(self):
        self.args = self.parse_args()
        super(Service, self).__init__(locals())

    def start(self):
        while self.alive:
            self.process()
            time.sleep(1)

    def process(self):
        print("程序正在执行")

    def parse_args(self):
        self.parser = ArgumentParser(conflict_handler="resolve")
        self.enrich_parser_arguments()
        return self.parser.parse_args()


Service().start()