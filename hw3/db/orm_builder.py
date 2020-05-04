from db.orm_model import Base, Log, Test
from db.orm_client import MysqlOrmConnection


class MysqlOrmBuilder:
    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.engine = self.connection.engine

    def create_db(self, t_name):
        if not self.engine.dialect.has_table(self.engine, t_name):
            Base.metadata.tables[t_name].create(self.engine)

    def add_elem(self, test_name):
        self.create_db('test')
        elem = Test(
            name=test_name,
        )
        self.connection.session.add(elem)
        self.connection.session.commit()


class MysqlOrmLogBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.engine = self.connection.engine

    def create_log_db(self):
        if not self.engine.dialect.has_table(self.engine, 'log'):
            Base.metadata.tables['log'].create(self.engine)

    def add_log(self, loglines):
        for line in loglines:
            try:
                log = Log(
                    remote_addr=line[0],
                    remote_user=line[1],
                    time_local=line[3]+' '+line[4],
                    request=line[5],
                    status=line[6],
                    body_bytes_sent=line[7],
                    http_referer=line[8],
                    http_user_agent=line[9],
                )
                self.connection.session.add(log)
            except IndexError:
                print('Line doesn\'t match DB format')
                print(line)
        self.connection.session.commit()
