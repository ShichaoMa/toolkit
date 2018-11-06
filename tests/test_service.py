from toolkit import test_prepare
test_prepare()
from toolkit.monitors import Service


class A(Service):
    def __init__(self):
        super(A, self).__init__()
        self.bbbb = self.args.bbbb
        print(self.bbbb)

    def enrich_parser_arguments(self):
        super(A, self).enrich_parser_arguments()
        self.parser.add_argument("-b", "--bbbb", help="Run backend. ")

    def start(self):
        import time
        while self.alive:
            time.sleep(1)
a = A()

print(a.settings)

a.start()
