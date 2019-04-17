import pytest

from toolkit.structures.linked_list import LinkedList


class TestLinkList(object):

    def test_init(self):
        lst = LinkedList([1, 2, 3, 4])
        assert list(lst) == [1, 2, 3, 4]

    def test_reverse_iter(self):
        lst = LinkedList([1, 2, 3, 4])
        assert list(lst.reverse_iter()) == [4, 3, 2, 1]

    def test_pop(self):
        lst = LinkedList([1, 2, 3, 4])
        for i in range(len(lst)):
            assert lst.pop(0) == i + 1

    def test_pop_reverse(self):
        lst = LinkedList([1, 2, 3, 4])
        for i in range(len(lst)-1, -1, -1):
            assert lst.pop(-1) == i + 1

    def test_get(self):
        lst = LinkedList([1, 2, 3, 4])
        assert lst[0] == 1
        assert lst[1] == 2
        assert lst[2] == 3
        assert lst[3] == 4

    def test_remove(self):
        lst = LinkedList([1, 2, 3, 4])
        assert lst.remove(3)
        assert list(lst) == [1, 2, 4]
        with pytest.raises(ValueError):
            lst.remove(3)

    def test_find(self):
        lst = LinkedList([1, 2, 3, 4])
        assert lst.find(3) == 2

        with pytest.raises(ValueError):
            lst.find(3, 0, 2)

    def test_in(self):
        lst = LinkedList([1, 2, 3, 4])
        assert 3 in lst

    def test_slice(self):
        lst = LinkedList([1, 2, 3, 4, 5])
        assert lst[:] == lst
        assert lst[1:2] == LinkedList([2])
        assert lst[::2] == LinkedList([1, 3, 5])
        assert lst[::-2] == LinkedList([5, 3, 1])
        assert lst[::-1] == LinkedList(lst.reverse_iter())
        lst[1:2] = [3, 4, 5]
        assert lst == LinkedList([1, 3, 4, 5, 3, 4, 5])
        lst[3:2] = [3, 4, 5]
        assert lst == LinkedList([1, 3, 4, 3, 4, 5, 5, 3, 4, 5])
        lst[:] = [1, 2, 3, 4]
        assert lst == LinkedList([1, 2, 3, 4])
        lst[4: 10] = [6, 7, 8]
        assert lst == LinkedList([1, 2, 3, 4, 6, 7, 8])

    def test_insert(self):
        lst = LinkedList([1, 2, 3, 4, 5])
        lst.insert(0, 10)
        assert list(lst) == [10, 1, 2, 3, 4, 5]

    def test_iadd(self):
        default = LinkedList([1, 2, 3, 4, 5])
        lst = default
        lst += [3, 4, 5, 6]
        assert lst == LinkedList([1, 2, 3, 4, 5, 3, 4, 5, 6])
        assert lst is default

    def test_add(self):
        lst = LinkedList([1, 2, 3, 4, 5])
        new_list = lst + [4, 5, 6]
        assert new_list is not lst
        assert new_list == LinkedList([1, 2, 3, 4, 5, 4, 5, 6])
        new_list2 = [4, 5, 6] + lst
        assert new_list2 == LinkedList([4, 5, 6, 1, 2, 3, 4, 5])
