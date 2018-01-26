import re
import ast
import json
import requests

from abc import abstractmethod
from collections import defaultdict

from ..singleton import SingletonABCMeta

from .. import unsigned_right_shitf, shift_left_for_js, shift_right_for_js

__all__ = ["TokenAcquirer"]


class TokenAcquirer(metaclass=SingletonABCMeta):

    def __init__(self, host, session):
        self.session = session
        self.key = None
        self.host = host if 'http' in host else 'https://' + host

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def n(self, r, o):
        pass

    def adjust(self, text):
        return text

    def __enter__(self):
        if not self.key:
            self.update()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.update()
        return exc_type is None

    def acquire(self, text):
        if not self.key:
            self.update()
        text = self.adjust(text)
        S = list()
        v = 0
        for ch in text:
            A = ord(ch)
            if 128 > A:
                S.append(A)
            elif 2048 > A:
                S.append(shift_right_for_js(A, 6) | 192)
            elif 55296 == (64512 & A) and v + 1 < len(text) and 56320 == (64512 & ord(text[v + 1])):
                A = 65536 + shift_left_for_js((1023 & A), 10) + (1023 & ord(text[v]))
                S.append(shift_right_for_js(A, 18) | 240)
                S.append(shift_right_for_js(A, 12) & 63 | 128)
                S.append(63 & A | 128)
            else:
                S.append(shift_right_for_js(A, 12) | 224)
                S.append(shift_right_for_js(A, 6) & 63 | 128)
                S.append(63 & A | 128)
        m, s = self.key.split(".")
        m = int(m)
        s = int(s)
        r = m
        for b in S:
            r = r + b
            r = self.n(r, '+-a^+6')
        r = self.n(r, '+-3^+b+-f')
        r ^= s
        if 0 > r:
            r = (2147483647 & r) + 2147483648

        r %= 1e6
        return "%s.%s" % (int(r), int(r) ^ m)

    @staticmethod
    def n(r, o):
        for t in range(0, len(o) - 2, 3):
            a = o[t + 2]
            a = ord(a) - 87 if a >= "a" else int(a)
            a = unsigned_right_shitf(r, a) if "+" == o[t + 1] else r << a
            r = r + a & 4294967295 if "+" == o[t] else r ^ a
        return r

    @classmethod
    def from_session(cls, host, session):
        return cls(host, session)


class BingAcquirer(TokenAcquirer):

    session_proxies = defaultdict(requests.cookies.RequestsCookieJar)

    def __init__(self, host, session):
        super(BingAcquirer, self).__init__(host, session)
        self.key = "0"

    def acquire(self, text):
        code = 0
        for i in text:
            i = ord(i)
            code = shift_left_for_js(code, 5) - code + i | 0
        return code

    def update(self):
        self.session.get("https://cn.bing.com/translator/", proxies=self.proxies)
        self.session_proxies[json.dumps(self.proxies)] = self.session.cookies

    @classmethod
    def from_session(cls, host, session, proxies=None):
        bing = cls(host, session)
        bing.proxies = proxies
        cookies = cls.session_proxies[json.dumps(proxies)]
        session.cookies = cookies
        bing.session = session
        return bing


class BaiduAcquirer(TokenAcquirer):

    def __init__(self, host, session=None):
        super(BaiduAcquirer, self).__init__(host, session)
        self.token = None

    def update(self):
        resp = self.session.post(self.host)
        self.token = re.search(r"token: '(\w+)'", resp.text).group(1)
        self.key = re.search(r"window.gtk = '(.*?)'", resp.text).group(1)

    def adjust(self, text):
        if len(text) > 30:
            return text[0: 10] + text[len(text) // 2 - 5: len(text) // 2 + 5] + text[-10:]
        return super(BaiduAcquirer, self).adjust(text)


class GoogleAcquirer(TokenAcquirer):
    RE_TKK = re.compile(r'TKK=eval\(\'\(\(function\(\)\{(.+?)\}\)\(\)\)\'\);', re.DOTALL)

    def update(self):
        r = self.session.get(self.host)
        code = str(self.RE_TKK.search(r.text).group(1)).replace('var ', '')
        code = code.encode().decode('unicode-escape')

        if code:
            tree = ast.parse(code)
            visit_return = False
            operator = '+'
            n, keys = 0, dict(a=0, b=0)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = node.targets[0].id
                    if name in keys:
                        if isinstance(node.value, ast.Num):
                            keys[name] = node.value.n
                        # the value can sometimes be negative
                        elif isinstance(node.value, ast.UnaryOp) and \
                                isinstance(node.value.op, ast.USub):  # pragma: nocover
                            keys[name] = -node.value.operand.n
                elif isinstance(node, ast.Return):
                    # parameters should be set after this point
                    visit_return = True
                elif visit_return and isinstance(node, ast.Num):
                    n = node.n
                elif visit_return and n > 0:
                    # the default operator is '+' but implement some more for
                    # all possible scenarios
                    if isinstance(node, ast.Add):  # pragma: nocover
                        pass
                    elif isinstance(node, ast.Sub):  # pragma: nocover
                        operator = '-'
                    elif isinstance(node, ast.Mult):  # pragma: nocover
                        operator = '*'
                    elif isinstance(node, ast.Pow):  # pragma: nocover
                        operator = '**'
                    elif isinstance(node, ast.BitXor):  # pragma: nocover
                        operator = '^'
            # a safety way to avoid Exceptions
            clause = compile('{1}{0}{2}'.format(
                operator, keys['a'], keys['b']), '', 'eval')
            value = eval(clause, dict(__builtin__={}))
            self.key = '{}.{}'.format(n, value)
