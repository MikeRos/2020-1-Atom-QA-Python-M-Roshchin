import pytest


class TestList:
    def test_list_concatenate(self):
        a = [0]
        b = [1]
        assert a + b == [0, 1]

    def test_list_slice(self):
        a = [1, 2, 3]
        a = a[1:2]
        assert a == [2]

    @pytest.mark.parametrize('i', range(0, 3))
    def test_list_3(self, i):
        a = [0]
        b = i
        a.append(b)
        assert a == [0, i]

    def test_list_reverse(self):
        a = [1, 2, 3]
        a = a[::-1]
        assert a == [3, 2, 1]

    def test_list_from_set(self):
        a = {1, 2, 3}
        b = list(a)
        assert b == [1, 2, 3]
