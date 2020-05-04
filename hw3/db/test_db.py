import pytest

from db.orm_client import MysqlOrmConnection
from db.orm_builder import MysqlOrmBuilder


def test_db():
    client = MysqlOrmConnection('test', 'testpass', 'TEST_DB')
    builder = MysqlOrmBuilder(client)
    name = 'NAME FOR TEST'
    builder.add_elem(name)
    assert client.execute_query('select * from test')[0][1] == name
