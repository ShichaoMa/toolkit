class Tree(object):

    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

    def __iter__(self):
        if self.left:
            yield from iter(self.left)
        yield self.data
        if self.right:
            yield from iter(self.right)


def make_operator_tree(operators):
    stack = []
    for operator in operators:
        tree = Tree(operator, None, None)
        if not operator.isalpha():
            tree.right = stack.pop()
            tree.left = stack.pop()
        stack.append(tree)
    return stack.pop()


if __name__ == "__main__":
    for data in make_operator_tree("ab+cde+**"):
        print(data, end="")