import pytest


class TestInt:
    def test_int_sum(self):
        a = 13
        b = -4
        assert a + b == 9

    def test_int_sign(self):
        a = 42
        assert a > 0
        a = 0
        assert a == 0
        a = -33
        assert a < 0

    def test_int_abs(self, random_sign, random_int):
        a = random_sign * random_int
        if a < 0:
            b = -a
        else:
            b = a
        assert abs(a) == b

    def test_int_cast(self):
        a = '42'
        a = int(a)
        assert isinstance(a, int)

    @pytest.mark.parametrize('a', range(0, 7))
    def test_int_reminder(self, a):
        assert a % 1 == 0
