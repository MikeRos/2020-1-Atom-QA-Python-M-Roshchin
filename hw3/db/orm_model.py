from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Test(Base):
    __tablename__ = 'test'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)


class Log(Base):
    __tablename__ = 'log'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    remote_addr = Column('remote_addr', String(50), nullable=False)
    remote_user = Column('remote_user', String(50), nullable=False)
    time_local = Column('time_local', String(50), nullable=False)
    request = Column('request', String(50), nullable=False)
    status = Column('status', Integer, nullable=False)
    body_bytes_sent = Column('body_bytes_sent', Integer, nullable=False)
    http_referer = Column('http_referer', String(50), nullable=False)
    http_user_agent = Column('http_user_agent', String(50), nullable=False)  # Includes http_x_forwarded_for"
