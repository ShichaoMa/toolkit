class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __iter__(self):
        cur = self
        while cur:
            yield cur.val
            cur = cur.next

    def __str__(self):
        string = "["
        for i in self:
            string += str(i)
            string += ","
        string += "]"
        return string

    __repr__ = __str__


class Solution:
    # 返回合并后列表
    def Merge(self, pHead1, pHead2):
        # write code here
        pre = None
        one = pHead1
        two = pHead2
        while pHead1 and pHead2:
            while pHead1 and pHead2 and pHead1.val < pHead2.val:
                pre = pHead1
                pHead1 = pHead1.next
            if pre:
                pre.next = pHead2
                pHead2 = pre
            while pHead1 and pHead2 and pHead1.val >= pHead2.val:
                pre = pHead2
                pHead2 = pHead2.next
            if pre and pHead1:
                pre.next = pHead1
                pHead1 = pre

        if pHead1:
            return two
        else:
            return one


def create(arr):
    pre = None
    cur = None

    for i in arr:
        node = ListNode(i)
        if pre:
            pre.next = node
        else:
            cur = node
        pre = node

    return cur


if __name__ == "__main__":
    print(Solution().Merge(create([1, 3, 5]), create([1, 3, 5])))
