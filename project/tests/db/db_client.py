import sqlalchemy
from sqlalchemy.orm import sessionmaker
from connections import DB_HOST, DB_PORT, DB_USERNAME, DB_USERPASS, DB_NAME


class DBClient:

    def __init__(self, user=DB_USERNAME, password=DB_USERPASS, db_name=DB_NAME):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = DB_HOST
        self.port = DB_PORT

        self._engine = sqlalchemy.create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=self.user,
                                                                          password=self.password,
                                                                          host=self.host,
                                                                          port=self.port,
                                                                          db=self.db_name),
            encoding='utf8'
        )

        session = sessionmaker(bind=self._engine, autoflush=True, enable_baked_queries=False, expire_on_commit=True)
        self._session = session()

    def get_session(self):
        self._session.expire_all()
        return self._session
