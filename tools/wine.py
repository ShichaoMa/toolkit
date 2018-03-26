# -*- coding:utf-8 -*-
from fractions import Fraction
from toolkit import cache_property
from functools import reduce


class Cup(object):
    """
    倒酒案例
    往一个二维酒杯塔里面倒酒，上层杯子满了之后，会流入下层，不考虑酒会丢失的情况。结构为
              cap
            cap cap
          cap cap cap
            ......
    求：倒入count杯酒时，第line行第col列杯中的酒量。
    """
    _total = set()

    def __init__(self, left_parent, right_parent, capacity):
        self.left_parent = left_parent
        self.right_parent = right_parent
        self.capacity = capacity

    @cache_property
    def right_child(self):
        return Cup(self, self.right_sibling, 0)

    @cache_property
    def left_child(self):
        if self.left_sibling:
            return self.left_sibling.right_child
        else:
            return Cup(self.left_sibling, self, 0)

    @cache_property
    def left_sibling(self):
        if self.left_parent:
            return self.left_parent.left_child
        else:
            return None

    @cache_property
    def right_sibling(self):
        if self.right_parent:
            return self.right_parent.right_child
        else:
            return None

    def pour(self, count):
        self._total.add(self)
        remainder = self.capacity + count - 1
        if remainder > 0:
            self.capacity = 1
            self.left_child.pour(remainder/2)
            self.right_child.pour(remainder/2)
        else:
            self.capacity += count

    def find(self, line, col):
        that = self
        for i in range(line-1):
            that = that.left_child

        for j in range(col-1):
            that = that.right_sibling

        return that

    def total(self):
        return reduce(lambda x, y: x+y, [i.capacity for i in self._total])

    def __str__(self):
        return str(Fraction(self.capacity))

    __repr__ = __str__

    def print(self, line, col):
        find = None
        blunk_f = "{:^%s}" % (line * 15)
        ele_f = " {:-^13} "
        this = self

        for i in range(line):
            that = this
            string = ele_f.format(str(that))
            count = 1

            while that.right_sibling:
                count += 1
                that = that.right_sibling

                if i == line - 1 and count == col:
                    string += ele_f.replace("-", "=").format(str(that))
                    find = that
                else:
                    string += ele_f.format(str(that))

            print(blunk_f.format(string))
            this = this.left_child

        if find:
            print(f"\n第{line}行,第{col}列杯子中的酒量为{find.capacity}。")


if __name__ == "__main__":
    import sys
    # 创建一个酒杯(塔)
    cup = Cup(None, None, 0)
    # 倒入酒
    cup.pour(int(sys.argv[1]))
    # 输出酒塔
    cup.print(int(sys.argv[2]), int(sys.argv[3]))
