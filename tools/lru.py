class Node(object):

    def __init__(self, val):
        self.val = val
        self.next = None


class Lru(object):

    def __init__(self, vals):
        self._head = None
        for val in vals:
            node = Node(val)
            if self._head:
                self._head.next = node
            else:
                self._head = node

    def hit(self, val):
        cur = self._head
        while cur:
            if cur.val == val and cur is not self._head:
                next = cur.next
                if next:
                    cur.next = next.next
                    cur.next.next = cur
                    next.next = self._head
                    self._head = next
                    return True
            elif cur is not self._head:
                return True

        return False
