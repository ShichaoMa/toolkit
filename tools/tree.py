class Node(object):

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def insert(self, data):
        if data > self.data:
            if self.right:
                self.right.insert(data)
            else:
                self.right = Node(data)
        elif data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = Node(data)

    def find_max(self):
        if not self.right:
            return self.data
        else:
            return self.right.find_max()

    def find_min(self):
        if not self.left:
            return self.data
        else:
            return self.left.find_max()

    def remove(self, data):
        if data == self.data:
            if self.left:
                self.data = self.left.find_max()
                self.left.remove(self.data)
            elif self.right:
                self.data = self.right.find_min()
                self.right.remove(self.data)
            else:
                self.data = None
            return True
        elif data < self.data:
            if self.left:
                return self.left.remove(data)
            else:
                return False
        else:
            if self.right:
                return self.right.remove(data)
            else:
                return False

    def __contains__(self, item):
        if self.data == item:
            return True
        elif item < self.data:
            return item in self.left
        else:
            return item in self.right

    def __len__(self):
        l = 1
        if self.right:
            l += len(self.right)
        if self.left:
            l += len(self.left)
        return l


class Tree(object):

    def __init__(self):
        self.root = None

    def __len__(self):
        if self.root:
            return len(self.root)
        else:
            return 0

    def __contains__(self, item):
        if self.root:
            return item in self.root
        else:
            return False

    def insert(self, data):
        node = Node(data)
        if self.root:
            self._insert(self.root, node)
        else:
            self.root = node

    def _insert(self, root, node):
        if node > root:
            if root.right:
                self._insert(root.right, node)
            else:
                root.right = node
        elif node < root:
            if root.left:
                self._insert(root.left, node)
            else:
                root.left = node

    def find_max(self):
        if not self.root:
            raise Exception("No data.")
        else:
            self.root.find_max()

    def remove(self, data):


    def _remove(self, node, data):
        if node.data == data:

        if self.root:
            result = self.root.remove(data)
            if self.root.data is None:
                self.root = None
            return result
        else:
            return False