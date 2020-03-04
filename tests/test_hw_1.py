"""First homework test module"""
import pytest
from fixtures.some_fixtures import random_int, random_sign


class TestList:
    def test_list_concatenate(self):
        a = [0]
        b = [1]
        assert isinstance(a, list) and isinstance(a, list) and a + b == [0, 1]

    def test_list_slice(self):
        a = [1, 2, 3]
        a = a[1:2]
        assert isinstance(a, list) and a == [2]

    @pytest.mark.parametrize('i', range(0, 3))
    def test_list_3(self, i):
        a = [0]
        b = i
        a.append(b)
        assert isinstance(a, list) and a == [0, i]

    def test_list_reverse(self):
        a = [1, 2, 3]
        a = a[::-1]
        assert isinstance(a, list) and a == [3, 2, 1]

    def test_list_from_set(self):
        a = {1, 2, 3}
        b = list(a)
        assert isinstance(a, set) and isinstance(b, list) and b == [1, 2, 3]


class TestSet:
    def test_set_add(self):
        a = {1, 2, 3}
        a.add(3)
        a.add(4)
        assert isinstance(a, set) and a == {1, 2, 3, 4}

    def test_set_insertion_upd(self):
        a = {1, 2, 3}
        b = {3, 4, 5}
        a &= b
        assert isinstance(a, set) and a == {3}

    def test_set_copy(self):
        a = {1, 2, 3}
        b = a.copy()
        c = a
        assert \
            isinstance(a, set) and isinstance(a, set) and isinstance(c, set) \
            and a is c and a is not b

    @pytest.mark.parametrize('i', range(1, 3))
    def test_set_is_in(self, i):
        a = {0, 1, 2, 3, 4, 5}
        assert isinstance(a, set) and i in a

    def test_set_subset(self):
        a = {1, 2, 3}
        b = {0, 1, 2, 3, 4, 5}
        assert isinstance(a, set) and isinstance(a, set) and a <= b


class TestDict:
    def test_dict(self):
        a = {'one': 1, 'two': 2, 'three': 3}
        assert isinstance(a, dict) and a == {"one": 1, "two": 2, "three": 3}

    @pytest.mark.parametrize('i', range(1, 4))
    def test_dict_key(self, i):
        a = {1: 'one', 2: 'two', 3: 'three'}
        assert isinstance(a, dict) and a[i]

    def test_dict_clear(self):
        a = {1: 'one', 2: 'two', 3: 'three'}
        a.clear()
        assert isinstance(a, dict) and a == dict()

    def test_dict_get(self):
        a = {1: 'one', 2: 'two', 3: 'three'}
        assert isinstance(a, dict) and a.get(2) == 'two'

    def test_dict_len(self):
        a = {1: 'one', 2: 'two', 3: 'three'}
        assert isinstance(a, dict) and len(a) == 3


class TestString:
    def test_string_quotes(self):
        a = 'some string'
        b = "some string"
        c = """some string"""
        assert isinstance(a, str) and isinstance(b, str) and isinstance(c, str) and a == b == c

    @pytest.mark.parametrize('s', ('P', 'y', 't', 'h', 'o', 'n'))
    def test_string_in(self, s):
        assert isinstance(s, str) and s in 'Python'

    def test_string_concatenate(self):
        a = 'str '
        i = 1
        a += str(i)
        assert a == 'str {}'.format(i)

    def test_string_strip(self):
        assert 'qwertyXstringXqwerty'.strip('qwertyX') == 'string'

    def test_string_5(self):
        assert 'abcdefg'.upper().isupper()


class TestInt:
    def test_int_sum(self):
        a = 13
        b = -4
        assert isinstance(a, int) and isinstance(b, int) and a + b == 9

    def test_int_sign(self):
        a = 42
        assert isinstance(a, int) and a > 0
        a = 0
        assert isinstance(a, int) and a == 0
        a = -33
        assert isinstance(a, int) and a < 0

    def test_int_abs(self, random_sign, random_int):
        a = random_sign * random_int
        if a < 0:
            b = -a
        else:
            b = a
        assert isinstance(a, int) and isinstance(b, int) and abs(a) == b

    def test_int_cast(self):
        a = '42'
        a = int(a)
        assert isinstance(a, int)

    @pytest.mark.parametrize('a', range(0, 7))
    def test_int_reminder(self, a):
        assert isinstance(a, int) and a % 1 == 0
