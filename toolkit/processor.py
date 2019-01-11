# -*- coding:utf-8 -*-
from functools import reduce
from contextlib import contextmanager


class Processor(object):
    """
    进度管理器，管理收集指定区域业务逻辑流程中的进度执行情况，如现有一个函数执行某个功能，
    现需要掌握其执行进度，假设其整个流程可分为三步，分别是三个函数调用，其中进度权重大约是
    1:2:3，则创建一个processor，指定其weight为[1, 2, 3]，将processor传入该函数，并在
    该函数完成每步进行processor.update调用来更新进度，调用三次，则进度到达100%，
    如果每步的子函数需要进一步划分进度，则通过调用：

    .. code-block:: python

        with processor.hand_out(weight) as child_processor
            child_function(..., child_processor)

    child_processor将负责将该步的进度按权重分发到子函数中去。
    """

    def __init__(self, weight, update_callback, _from=0, to=100, skip=None):
        """

        :param weight: 将一个函数分成的工作区块数，如果是int类型，则是区作区块数，
            如果是[1, 4, 6...]类型，则指定了每个工作区块的工作量权重。
        :param update_callback: 当完成规定的进度后，调用的函数
        :param _from:
        :param to:
        :param skip:
        """
        assert weight, "Weight cannot be empty! Got: %s" % weight
        assert _from < to, "Process should be increase! Got: %s-%s" % (_from, to)
        if isinstance(weight, int):
            weight = [1] * weight

        self.processes = self.split(weight, _from, to)
        self.update_callback = update_callback
        self.last_process = _from
        self._skip = skip

    def can_update(self, current_process):
        return not (self._skip and self._skip(current_process))

    def skip(self):
        """
        通过判断下一个进度值是否小于当前进度来决定是否跳过
        @return:
        """
        return not self.can_update(self.processes[0])

    def skip_all(self):
        """
        如果派生了子进度条，则通过判断子进度最大进度值来决定是否直接跳过子进度条
        @return:
        """
        return not self.can_update(self.processes[-1])

    @staticmethod
    def split(weight, _from, to):
        count = sum(weight)
        distance = float(to - _from)
        step = distance / float(count)
        if step == 0:
            return [0] * len(weight)
        else:
            processes = []
            reduce(lambda w1, w2: processes.append(
                int(_from + step*(w1 + w2))) or w1 + w2, weight, 0)
            return processes

    def update(self, message=None):
        """
        将进度更新到下一个进度值
        @param message:
        @return:
        """
        current_process = self.processes.pop(0)
        if self.can_update(current_process) and current_process != self.last_process:
            if message:
                self.update_callback(current_process, message)
            else:
                self.update_callback(current_process)
        self.last_process = current_process

    @contextmanager
    def hand_out(self, weight):
        """
        为子函数派生子进度条，子进度条根据权重分配父进度其中一个工作区块对应的进度区间
        @param weight:
        @return:
        """
        current_process = self.processes.pop(0)
        child = self.__class__(
            weight, self.update_callback,
            self.last_process, current_process, self._skip)
        yield child
        self.last_process = current_process


class AsyncProcessor(Processor):
    """
    update方法变为异步的形式
    """

    async def update(self, message=None):
        """
        将进度更新到下一个进度值

        @param message:
        @return:
        """
        current_process = self.processes.pop(0)
        if self.can_update(current_process) and current_process != self.last_process:
            if message:
                await self.update_callback(current_process, message)
            else:
                await self.update_callback(current_process)
        self.last_process = current_process