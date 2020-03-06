import random
import pytest


@pytest.fixture()
def random_int():
    yield random.randint(0, 1000)


@pytest.fixture()
def random_sign():
    yield (-1)**random.randint(0, 1)
