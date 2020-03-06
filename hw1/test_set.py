import pytest


class TestSet:
    def test_set_add(self):
        a = {1, 2, 3}
        a.add(3)
        a.add(4)
        assert a == {1, 2, 3, 4}

    def test_set_insertion_upd(self):
        a = {1, 2, 3}
        b = {3, 4, 5}
        a &= b
        assert a == {3}

    def test_set_copy(self):
        a = {1, 2, 3}
        b = a.copy()
        c = a
        assert a is c and a is not b

    @pytest.mark.parametrize('i', range(1, 3))
    def test_set_is_in(self, i):
        a = {0, 1, 2, 3, 4, 5}
        assert i in a

    def test_set_subset(self):
        a = {1, 2, 3}
        b = {0, 1, 2, 3, 4, 5}
        assert a <= b
