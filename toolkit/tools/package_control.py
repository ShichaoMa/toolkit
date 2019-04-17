import re
import os

from functools import partial
from argparse import ArgumentParser


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    mth = re.search(r"__version__\s?=\s?['\"]([^'\"]+)['\"]", init_py)
    if mth:
        return mth.group(1)
    else:
        raise RuntimeError("Cannot find version!")


def install_requires():
    """
    Return requires in requirements.txt
    :return:
    """
    try:
        with open("requirements.txt") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except OSError:
        return []


def change_version(index=None, dev=False, package_name=None):

    if not index:
        parser = ArgumentParser()
        parser.add_argument("-i", "--index", type=int, help="版本顺位", default=3)
        parser.add_argument("-d", "--dev", action="store_true", help="是否是开发模式")
        args = parser.parse_args()
        index = args.index
        dev = args.dev

    package = package_name or os.path.basename(os.path.abspath(os.getcwd())).replace("-", "_")
    with open(os.path.join(package, '__init__.py'), "r+", encoding="utf-8") as f:
        init_py = f.read()
        f.seek(0)
        buf = re.sub(
            r"(__version__\s?=\s?['\"])([^'\"]+)(['\"])",
            partial(_repl, index=int(index), dev=dev), init_py)
        f.write(buf)


def _repl(mth, index, dev):
    versions = mth.group(2).split(".")
    vs = versions[index - 1]
    length = len(vs)

    if vs.isdigit():
        new_vs = str(int(vs) + 1) + ("dev1" if dev else "")
    else:
        def _rep(mth, dev):
            string = mth.group(1)
            # 如果是版本开始，如：1d1中的第一个1，那么无论是否dev，1都可以保持不变。
            # 否则，则是第二个1或者d，当是dev=False时，这些都是要被舍弃的(正式版不含dev)
            # 只dev=True且是第二个1时，才需要自增1，如果是d，那么保持不变就可以。
            if mth.start():
                if dev:
                    if string.isdigit():
                        return str(int(string) + 1)
                else:
                    return ""

            return string

        new_vs = re.sub(r"(\d+|[a-zA-Z]+)",  partial(_rep, dev=dev), vs)
        if not new_vs[-1].isdigit():
            new_vs += "1"
    versions[index - 1] = new_vs
    blank = (length - len(new_vs)) * " "

    # 如果不是第三位+1。而是第二位或得第一位，则后续的位数应该清0
    for i in range(index, len(versions)):
        blank += " " * (len(versions[i]) - 1)
        versions[i] = "0"

    return mth.group(1) + ".".join(versions) + mth.group(3) + blank