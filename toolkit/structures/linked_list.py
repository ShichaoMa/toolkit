class Node(object):
    """
    链表的节点
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)

    __repr__ = __str__


class Iterator(object):
    """
    迭代器的实现
    """
    def __init__(self, current_node, towards="right"):
        self.current_node = current_node
        self.towards = towards

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_node:
            value = self.current_node.value
        else:
            raise StopIteration()
        self.current_node = getattr(self.current_node, self.towards)
        return value


class LinkedList(object):
    """
    链表
    """
    def __init__(self, iterable):
        self.head = None
        self.tail = None
        self._size = 0
        last_node = self._iadd(iterable)

        if last_node is not None:
            self.tail = last_node

    def _iadd(self, iterable, last_node=None):
        """
        自增逻辑
        :param iterable: 被加的可迭代对象
        :param last_node:
        :return:
        """
        for val in iterable:
            last_node = Node(val, left=last_node)
            if last_node is None or last_node.left is None:
                self.head = last_node
            else:
                last_node.left.right = last_node
            self._size += 1
        return last_node

    def __len__(self):
        return self._size

    def __iter__(self):
        return Iterator(self.head)

    def insert(self, index, x):
        self._slice_setter(index, index, x)

    def reverse_iter(self):
        """
        反向迭代
        :return:
        """
        return Iterator(self.tail, "left")

    def __eq__(self, other):
        """
        判断两个对象是否相等
        :param other:
        :return:
        """
        if not isinstance(other, self.__class__):
            return False
        if self._size != len(other):
            return False

        for i, j in zip(self, other):
            if i != j:
                return False
        return True

    def __hash__(self):
        raise ValueError("Cannot hash!")

    def _adjust_index(self, index):
        """
        调整下标，统一成正数的形式，对于不合法的下标抛出异常
        :param index:
        :return:
        """
        if index >= self._size:
            raise IndexError(f"Index: {index}")
        else:
            now = (self._size + index)
            if now < 0:
                raise IndexError(f"Index: {index}")
            return now % self._size

    def __getitem__(self, key):
        if not isinstance(key, slice):
            return self._get_node(key).value
        else:
            return self.__class__(self._slice_parser(key))

    def _slice_setter(self, left, right, *sequence):
        """
        切片赋值逻辑
        :param left:
        :param right:
        :param sequence:
        :return:
        """
        # 先获取左边的节点，如果越界，则从整个链表右侧追加元素，直接返回
        try:
            left_node = self._get_node(left)
        except IndexError:
            self._iadd(sequence, self.tail)
            return
        # 如果右边的下标大于左边的，则认定为列表插入操作，直接将左右视为相同
        # 否则，获取右边的节点，若越界，则将右边节点置为None
        if right <= left:
            right_node = left_node
        else:
            try:
                right_node = self._get_node(right)
            except IndexError:
                right_node = None
        # 求左右的距离，这个距离内的节点会被覆盖掉
        distance = self._distance_between(left_node, right_node)
        # 对链表进行自增操作，从左边节点开始自增
        last_node = self._iadd(sequence, left_node.left)
        # 增加完毕后，记得将左边节点的引用置为空
        left_node.left = None
        # 对于右边结点为空的情况，此时右边部分已经全被覆盖了，所以tail需要换掉
        if right_node is None:
            self.tail = last_node
        # 否则，将右边节点和自增完的最后一个节点连接。
        else:
            last_node.right = right_node
            right_node.left = last_node
        # 最后调整链表的尺寸
        self._size -= distance

    @staticmethod
    def _distance_between(left, right):
        """
        求两个结点之间的距离
        :param left: 左边的node， 不能为null
        :param right: 右边的node，为null时为左边到最后的距离
        :return:
        """
        length = 0
        while left != right:
            left = left.right
            length += 1
        return length

    def __setitem__(self, key, value):
        if not isinstance(key, slice):
            self._get_node(key).value = value
        else:
            self._slice_setter(key.start or 0, key.stop or self._size, *value)

    def __iadd__(self, other):
        last_node = self._iadd(other, self.tail)
        if last_node is not None:
            self.tail = last_node
        return self

    def __add__(self, other):
        lst = self.__class__(self)
        lst += other
        return lst

    def __radd__(self, other):
        lst = self.__class__(other)
        lst += self
        return lst

    def _slice_parser(self, sl):
        """
        切片获取逻辑
        :param sl:
        :return:
        """
        # 对于未指定开始的，认为是从-1开始，注意，-1不是下标，因为-1的下标其实是_size-1
        start = sl.start or -1
        # 对于未指定结束的，则按结束为size，size同样也不是下标
        # 可以理解默认的start和stop都是链表两个下标的自减1和自加1，为什么这么设计呢，
        # 因为没写时候，该端点上的值是需要被完全迭代的，所以适当扩大该端点的范围是被请允许的。
        stop = sl.stop or self._size
        step = sl.step or 1
        # begin是开始的下标，对于递增的切片，begin应该是指定的开始和0的最大值，
        # 此时between的判断逻辑左闭右开。对于递减的切片，begin应该是指定的结束和
        # size-1的最小值，此时between的逻辑应该是左开右闭。

        if step > 0:
            begin = max(start, 0)
            between = self._get_between(True)
            iterator = zip(range(0, self._size), iter(self))
        else:
            begin = min(stop, self._size-1)
            between = self._get_between(False)
            iterator = zip(range(self._size-1, -1, -1), self.reverse_iter())

        # 迭代链表，其下标与链表本身同样递增或递减
        for i, val in iterator:
            # 如果下标在开始和结束之间，同时从开始计算步长合适，则yield值
            if between(i, start, stop) and (i - begin) % step == 0:
                yield val

    @staticmethod
    def _get_between(with_left=True):
        if with_left:
            return lambda index, left, right: left <= index < right
        else:
            return lambda index, left, right: left < index <= right

    def _get_node(self, index):
        if not isinstance(index, int):
            raise TypeError("Index type must be int!")
        index = self._adjust_index(index)
        node = self.head
        while index > 0:
            node = node.right
            index -= 1
        return node

    def _get_index_node_by_value(self, value, start=None, end=None):
        node = self.head
        index = 0
        if start is None:
            start = 0
        if end is None:
            end = self._size
        # 从头部开始查找等于目标值的节点，直到等于end时停止
        while index < end:
            if index >= start and node.value == value:
                return index, node

            node = node.right
            index += 1

        raise ValueError(f"Value: {value} not found!")

    def remove(self, value):
        _, node = self._get_index_node_by_value(value)
        return self._remove_node(node)

    def find(self, value, start=None, end=None):
        index, node = self._get_index_node_by_value(value, start, end)
        return index

    def pop(self, index=-1):
        node = self._get_node(index)
        self._remove_node(node)
        return node.value

    def _remove_node(self, node):
        # 如果该节点存在左边节点，则将该节点左边的节点指向该节点
        if node.left:
            node.left.right = node.right
        # 否则证明这是头部
        else:
            self.head = node.right

        # 同上
        if node.right:
            node.right.left = node.left
        else:
            self.tail = node.left

        self._size -= 1
        return True

    def __str__(self):
        if not self:
            return "[]"
        string = "["
        for i in self:
            string += "%r, " % i
        return string[:-2] + "]"

    __repr__ = __str__
