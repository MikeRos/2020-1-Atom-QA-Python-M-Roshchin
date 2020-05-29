from sqlalchemy import Column, Integer, String, DATETIME, SMALLINT, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    username = Column(String(16), default=None)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False)
    access = Column(SMALLINT, default=None)
    active = Column(SMALLINT, default=None)
    start_active_time = Column(DATETIME, default=None)

    UniqueConstraint(email, name='email')
    UniqueConstraint(username, name='ix_test_users_username')

    def __repr__(self):
        return f' ID: {self.id} Username: {self.username} Password: {self.password} ' \
               f'Email: {self.email} Access: {self.access} Active: {self.active} ' \
               f'Last login: {self.start_active_time}\n'
