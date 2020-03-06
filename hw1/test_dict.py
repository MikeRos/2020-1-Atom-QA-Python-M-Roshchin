import pytest


class TestDict:
    def test_dict(self):
        a = {'one': 1, 'two': 2, 'three': 3}
        assert a == {"one": 1, "two": 2, "three": 3}

    @pytest.mark.parametrize('i', range(1, 4))
    def test_dict_key(self, i):
        a = {1: 'one', 2: 'two', 3: 'three'}
        assert a[i]

    def test_dict_clear(self):
        a = {1: 'one', 2: 'two', 3: 'three'}
        a.clear()
        assert a == dict()

    def test_dict_get(self):
        a = {1: 'one', 2: 'two', 3: 'three'}
        assert a.get(2) == 'two'

    def test_dict_len(self):
        a = {1: 'one', 2: 'two', 3: 'three'}
        assert len(a) == 3
