from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, Enum, Date, Sequence, DateTime, Boolean, ForeignKey
import datetime

Base = declarative_base()

class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class TableNameIdMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    @declared_attr
    def id(cls):
        return Column(Integer, Sequence('{}_id_seq'.format(cls.__tablename__)), primary_key=True)


class PersonMixin(object):
    firstname = Column(String(50))
    lastname = Column(String(50))


class User(Base, TableNameIdMixin, PersonMixin):
    username = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)

    def __repr__(self):
        return "<User(firstname={}, lastname={}, id={})>".format(
            self.firstname, self.lastname, self.id)


class Dataset(Base, TableNameIdMixin):
    info = Column(String(10000), nullable=False)
    name = Column(String(50))


class DatasetRights(Base, TableNameIdMixin):
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    dataset_id = Column(Integer, ForeignKey('datasets.id'), nullable=False)
    read = Column(Boolean, nullable=False, default=False)
    write = Column(Boolean, nullable=False, default=False)
    delete = Column(Boolean, nullable=False, default=False)
