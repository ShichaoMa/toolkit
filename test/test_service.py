import sys
sys.path.insert(0, "/Users/mashichao/myprojects/toolkit")
from toolkit.monitors import Service


class Test(Service):
    def __init__(self):
        super(Test, self).__init__()
        from toolkit import debugger
        debugger()
        self.bbbb = self.args.bbbb
        print(self.bbbb)

    def enrich_parser_arguments(self):
        super(Test, self).enrich_parser_arguments()
        self.parser.add_argument("-b", "--bbbb", help="Run backend. ")
Test()