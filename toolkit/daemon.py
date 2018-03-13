import os
import re
import sys
import time
import signal
import warnings

from . import timeout

__all__ = ["daemon", "daemonize"]


def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """
    将进程变成守护进程
    :param stdin:
    :param stdout:
    :param stderr:
    :return:
    """
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            # 父进程退出
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # 从母体环境脱离
    # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。
    # 也可以改变到对于守护程序运行重要的文件所在目录
    os.chdir("/")
    # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.umask(0)
    # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。
    os.setsid()

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            # 第二个父进程退出
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # 进程已经是守护进程了，重定向标准文件描述符
    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+')
    # dup2函数原子化关闭和复制文件描述符
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


@timeout(5, "n")
def _t_raw_input(alive_pid):
    """重复启动时提示是否重启，5秒钟后超时返回n"""
    raw_input = globals().get("raw_input") or input
    return raw_input(
        "The process with pid %s is running, restart it? y/n: " % alive_pid)


def common_stop_start_control(
        parser, monitor_log_path, wait=2, allow_multi=False):
    warnings.warn(
        "common_stop_start_control is a deprecated alias,"
        " use daemonize instead.",
        DeprecationWarning, 2)
    return daemonize(parser, monitor_log_path, wait, allow_multi)


def daemonize(parser, monitor_log_path, wait=2, allow_multi=False):
    """
    开启关闭及守护进程方式启动的公共实现
    :param parser: 一个argparse命令行参数解析对象，其它参数请调用些函数之前声明
    :param monitor_log_path: 如果通过--daemon 守护进程的方式启动，
    需要提供守护进程的stdout, stderr的文件路径
    :param wait: 轮循发起关闭信号的间隔时间
    :param allow_multi: 是否允许开启多个进程
    :return: argparse的解析结果对象
    """
    parser.add_argument("-d", "--daemon", action="store_true", default=False)
    parser.add_argument(
        "method", nargs="?", choices=["stop", "start", "restart", "status"])
    args = parser.parse_args()
    pid = os.getpid()
    filter_process_name = "%s .*%s"%(sys.argv[0], "start")
    if args.method == "stop":
        _stop(filter_process_name, sys.argv[0], wait)
        sys.exit(0)
    if args.method == "status":
        alive_pid = _check_status(filter_process_name, [pid])
        prompt = ["PROCESS", "STATUS", "PID", "TIME"]
        status = [sys.argv[0].rstrip(".py"),
                  "RUNNING" if alive_pid else "STOPPED",
                  str(alive_pid), time.strftime("%Y-%m-%d %H:%M:%S")]
        for line in _format_line([prompt, status]):
            [print(i, end="") for i in line]
            print("")
        sys.exit(0)
    elif args.method == "restart":
        _stop(filter_process_name, sys.argv[0], wait, ignore_pid=[pid])
        print("Start new process. ")
    else:
        alive_pid = _check_status(filter_process_name, ignore_pid=[pid])
        if alive_pid and not allow_multi:
            result = _t_raw_input(alive_pid)
            if result.lower() in ["y", "yes"]:
                _stop(filter_process_name, sys.argv[0], wait, ignore_pid=[pid])
            else:
                sys.exit(0)
    if args.daemon:
        daemon(stdout=monitor_log_path, stderr=monitor_log_path)
    return args


def _format_line(lines):
    if not lines:
        return [""]
    max_lengths = [0]*len(lines[0])
    for line in lines:
        for i, ele in enumerate(line):
            max_lengths[i] = max(len(ele), max_lengths[i])
    new_lines = []
    for line in lines:
        new_line = []
        for i, ele in enumerate(line):
            new_line.append(ele.ljust(max_lengths[i]+1))
        new_lines.append(new_line)
    return new_lines


def _stop(name, default_name=None, timedelta=2, ignore_pid=[]):
    """
    关闭符合名字（regex)要求的进程
    :param name: regex用来找到相关进程
    :param default_name: 仅用做显示该进程的名字
    :param timedelta: 轮循发起关闭信号的间隔时间
    :param ignore_pid: 忽略关闭的进程号
    :return:
    """
    pid = _check_status(name, ignore_pid)
    if not pid:
        print("No such process named %s" % (default_name or name))
    while pid:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
        pid = _check_status(name, ignore_pid)
        if pid:
            print("Wait for %s exit. pid: %s" % (default_name or name, pid))
        time.sleep(timedelta)


def _check_status(name, ignore_pid):
    """
    找到主进程的pid
    :param name:
    :param ignore_pid:
    :return:
    """
    ignore = re.compile(r'ps -ef|grep')
    check_process = os.popen('ps -ef|grep "%s"' % name)
    processes = [x for x in check_process.readlines() if x.strip()]
    check_process.close()
    main_pid, main_ppid = None, None
    for process in processes:
        col = process.split()
        pid, ppid = col[1: 3]
        pid = int(pid) if int(pid) not in ignore_pid else None
        ppid = int(ppid)
        if not pid or ignore.search(process):
            continue
        main_pid, main_ppid = (pid, ppid) if not main_pid else \
            ((pid, ppid) if main_ppid == pid else (main_pid, main_ppid))
    return main_pid and (int(main_pid)
                         if int(main_pid) not in ignore_pid else None)

