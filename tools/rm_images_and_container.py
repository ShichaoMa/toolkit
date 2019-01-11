
# -*- coding:utf-8 -*-
import os
import re
import sys
from pdb import Pdb

regx = re.compile("(\S+)")


def fun(columns):
    return columns[1] == "<none>"


def rm_container():
    for line in os.popen("docker ps -a").readlines():
        columns = regx.findall(line)
        os.system("docker rm %s"%columns[0].strip())


def rm_image():

    def bar(columns):
        return columns[2]

    def rm(id):
        os.system("docker rmi %s"%id)

    [rm(bar(regx.findall(line))) for line in reversed(os.popen("docker images").readlines()) if fun(regx.findall(line))]


if __name__ == "__main__":
    eval("rm_%s()"%sys.argv[1])
