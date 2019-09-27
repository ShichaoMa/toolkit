import re
import os
import sys
import time
import signal

from socket import socket
from threading import Thread
from abc import ABCMeta
from _collections_abc import _check_methods

from .. import timeout
from .console import CustomInteractiveInterpreter, _local


class CommandlineAbility(metaclass=ABCMeta):

    @classmethod
    def add_commandline_arguments(cls, parser):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is CommandlineAbility:
            try:
                return _check_methods(C, "add_commandline_arguments")
            except AttributeError:
                return False
        return NotImplemented


class CommandlinePluginProxy(object):

    def __init__(self, plugin_cls, parser):
        assert issubclass(plugin_cls, CommandlineAbility), \
            "CommandlinePluginProxy only proxy CommandlineAbility class!"
        self.plugin_cls = plugin_cls
        self.parser = parser
        plugin_cls.add_commandline_arguments(parser)
        self.instance = None

    def __get__(self, instance, owner):
        if self.instance is None:
            args = self.parser.parse_args()
            self.instance = self.plugin_cls(args, instance)
        return self.instance


class Supervisor(CommandlineAbility):
    """
    管理进程的启动、状态、关闭，支持daemon化进程
    """
    def __init__(self, args, instance=None):
        self.is_daemon = args.daemon
        self.method = args.method

    def control(self, log_path='/dev/null', interval=2, allow_multi=False):
        filter_process_name = sys.argv[0].\
                                  replace(".py", "").\
                                  replace(os.getcwd(), "").\
                                  replace("/", ".*") + " .*start"
        if self.method == "stop":
            self._stop(filter_process_name, sys.argv[0], interval)
            sys.exit(0)

        if self.method == "status":
            alive_pid = self._find_alive_pid(filter_process_name)
            prompt = ["PROCESS", "STATUS", "PID", "TIME"]
            status = [sys.argv[0], "RUNNING" if alive_pid else "STOPPED",
                      str(alive_pid), time.strftime("%Y-%m-%d %H:%M:%S")]
            for line in self._format_line([prompt, status]):
                for i in line: print(i, end="")
                print("")
            sys.exit(0)

        if self.method == "restart":
            self._stop(filter_process_name, sys.argv[0], interval)
            print("Start new process. ")
        elif self.method == "start":
            alive_pid = self._find_alive_pid(filter_process_name)
            if alive_pid and not allow_multi:
                result = self._t_raw_input(alive_pid)
                if result.lower() in ["y", "yes"]:
                    self._stop(filter_process_name, sys.argv[0], interval)
                else:
                    sys.exit(0)

        if self.is_daemon:
            self.daemon(stdout=log_path, stderr=log_path)

    @classmethod
    def add_commandline_arguments(cls, parser):
        parser.add_argument("-d", "--daemon", action="store_true")
        parser.add_argument(
            "method", nargs="?", choices=["stop", "start", "restart", "status"])

    @staticmethod
    @timeout(10, "n")
    def _t_raw_input(alive_pid):
        """
        重复启动时提示是否重启，10秒钟后超时返回n
        """
        raw_input = globals().get("raw_input") or input
        return raw_input(
            "The process with pid %s is running, restart it? y/n: " % alive_pid)

    @staticmethod
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

    def _stop(self, name, default_name=None, timedelta=2):
        """
        关闭符合名字（regex)要求的进程
        :param name: regex用来找到相关进程
        :param default_name: 仅用做显示该进程的名字
        :param timedelta: 轮循发起关闭信号的间隔时间
        :return:
        """
        pid = self._find_alive_pid(name)
        if not pid:
            print("No such process named %s" % (default_name or name))

        while pid:
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass
            pid = self._find_alive_pid(name)
            if pid:
                print(f"Wait for {default_name or name} exit. pid: {pid}")
            time.sleep(timedelta)

    @staticmethod
    def _find_alive_pid(name):
        """
        找到主进程的pid
        :param name:
        :return:
        """
        ignore_pid = os.getpid()
        ignore = re.compile(r'ps -ef|grep')
        check_process = os.popen('ps -ef|grep -e "%s"' % name)
        processes = [x for x in check_process.readlines() if x.strip()]
        check_process.close()
        main_pid, main_ppid = None, None

        for process in processes:
            pid, ppid = [int(i) for i in process.split()[1:3]]
            if pid == ignore_pid or ignore.search(process):
                continue
            if not main_pid or main_ppid == pid:
                main_pid, main_ppid = pid, ppid

        return main_pid

    @staticmethod
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
            sys.stderr.write(
                "fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
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
            sys.stderr.write(
                "fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
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


class Console(CommandlineAbility):
    """
    通过交互客户端实时了解程序内部变化
    """
    alive = True

    def __init__(self, args, instance):
        if args.console:
            self._start_client(args.console_host, args.console_port)
        else:
            self.debug = args.debug
            self.namespace = locals()
            self.host = args.console_host
            self.port = args.console_port

    def init_console(self):
        if self.debug:
            console_thread = Thread(target=self._console)
            console_thread.setDaemon(True)
            console_thread.start()

    def _start_client(self, console_host, console_port):
        client = socket()
        client.connect((console_host, console_port))
        result = b""
        while self.alive:
            if not result.count(b"...") and result != b">>> ":
                print(">>> ", end="")
            try:
                cmd = input()
            except KeyboardInterrupt:
                break
            if not cmd:
                cmd = "\n"
            if cmd == "exit" or cmd == "exit()":
                break
            client.send(cmd.encode())
            result = client.recv(102400)
            if result:
                print(result.decode(),
                      end="" if result.count(b"...") or result == b">>> "
                      else "\n")
            else:
                break
        client.close()
        self.alive = False
        sys.exit(0)

    def _console(self):
        server = socket()
        server.setblocking(False)
        server.bind((self.host, self.port))
        server.listen(0)
        ci = CustomInteractiveInterpreter(self.namespace)
        _local._current_ipy = ci
        while self.alive:
            client = None
            try:
                client, addr = server.accept()
                while self.alive:
                    try:
                        cmd = client.recv(102400)
                        if not cmd:
                            break
                        result = ci.runsource(cmd.decode()).encode()
                        client.send(result)
                    except BlockingIOError as e:
                        time.sleep(0.1)
            except BlockingIOError as e:
                if not self.alive:
                    break
                time.sleep(1)
            finally:
                if client:
                    try:
                        client.close()
                    except:
                        pass
        server.close()
        self.alive = False

    @classmethod
    def add_commandline_arguments(cls, parser):
        parser.add_argument(
            "--debug", help="debug mode. ", action="store_true")
        parser.add_argument(
            "--console", help="start a console. ", action="store_true")
        parser.add_argument(
            "--console-host", help="console host. ", default="")
        parser.add_argument(
            "--console-port", type=int, help="console port. ", default=7878)
