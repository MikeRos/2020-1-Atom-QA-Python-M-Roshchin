from random import randint
import pytest


@pytest.fixture(scope='function')
def test_segment_data():
    data = {
        'name': f'test_name {randint(100, 100000)}',
        'pass_condition': 1,
        'relations': [
            {
                'object_type': "remarketing_player",
                'params': {"type": "positive", "left": 365, "right": 0}
            }
        ],
        'logicType': "or"
    }
    return data
