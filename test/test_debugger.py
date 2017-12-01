from toolkit import debugger
import os


def fun():
    os.environ["DEBUG"] = ""
    debugger()
    print(11111)


fun()