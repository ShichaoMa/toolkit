# -*- coding:utf-8 -*-
import json
import time
import requests

import asyncio
def crawl():

    resp = requests.post("http://0.0.0.0:9999/api/discover",
                         data={"data": json.dumps({"crawlid": "roc_%s"%time.strftime("%Y%m%d%H%M%S"),
                         "source_site_code": "FFCHCN", "full": True,
                         "url": "https://www.farfetch.cn/cn/shopping/men/buckled-shoes-2/items.aspx",
                         "meta": {"tags": {"source_site_code": "FFCHCN", "tags": [], "brand_id": 1,
                                           "gender_id": 1, "source_site_id": 1, "taxon_id": 3}}})})

    print(resp.text)
# class ApiTest(unittest.TestCase):
#
#     def test_feed(self):
#         self.assertEqual()

def tags():

    resp = requests.post("http://192.168.200.31:9999/api/enrich/tags",
                         data={"data": json.dumps({"source_site_code": "AMZN", "type": "ENRICH",
                         "url": "https://www.amazon.com/s/ref=lp_679337011_ex_n_10?rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A679337011%2Cn%3A6127767011&bbn=679337011&ie=UTF8",
                         "tags": ["aaa"]})})

    print(resp.text)


def update():
    resp = requests.post("http://0.0.0.0:9999/api/update",
                         json={
                         "site": "FFCHCN",
                         "full": True, "messages": [{"tags": [], "item_id": "", "meta": {"url": "https://www.farfetch.cn/cn/shopping/men/asics---item-12527082.aspx?storeid=9671&from=listing"}}]
                         })

    print(resp.text)



#
# update()


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
    求：倒入count杯酒时，第line行第col例杯中的酒量。
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

    def increase(self, count):
        self._total.add(self)
        remainder = self.capacity + count - 1
        if remainder > 0:
            self.capacity = Fraction(1, 1)
            self.left_child.increase(remainder/2)
            self.right_child.increase(remainder/2)
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


if __name__ == "__main__":
    # 创建一个酒杯(塔)
    cup = Cup(None, None, Fraction(0, 1))
    # 倒入105杯酒
    cup.increase(105)
    # 求第17行，第6列中的酒量
    print(cup.find(17, 6).capacity)
    print(cup.total())
