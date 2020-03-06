import pytest


class TestString:
    def test_string_quotes(self):
        a = 'some string'
        b = "some string"
        c = """some string"""
        assert a == b == c

    @pytest.mark.parametrize('s', ('P', 'y', 't', 'h', 'o', 'n'))
    def test_string_in(self, s):
        assert s in 'Python'

    def test_string_concatenate(self):
        a = 'str '
        i = 1
        a += str(i)
        assert a == 'str {}'.format(i)

    def test_string_strip(self):
        assert 'qwertyXstringXqwerty'.strip('qwertyX') == 'string'

    def test_string_5(self):
        assert 'abcdefg'.upper().isupper()
