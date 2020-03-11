from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum, Date, Sequence, DateTime, Boolean, ForeignKey, Table
import datetime

Base = declarative_base()


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class TableNameMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'


class TableIdMixin(object):
    @declared_attr
    def id(cls):
        return Column(Integer, Sequence('{}_id_seq'.format(cls.__tablename__)), primary_key=True)


class TableNameIdMixin(TableNameMixin, TableIdMixin):
    pass


class PersonMixin(object):
    firstname = Column(String(50))
    lastname = Column(String(50))


user_group_associations = Table('user_group_associations', Base.metadata,
                                Column('users_id', Integer, ForeignKey('users.id')),
                                Column('groups_id', Integer, ForeignKey('groups.id'))
                                )


class User(Base, TableNameIdMixin, PersonMixin):
    username = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)

    groups = relationship(
        "Group",
        secondary=user_group_associations,
        back_populates="users")

    def __repr__(self):
        return "<User(firstname={}, lastname={}, id={})>".format(
            self.firstname, self.lastname, self.id)


class Dataset_Group_Association(Base, TableNameMixin):
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'), primary_key=True)
    read = Column(Boolean, nullable=False, default=False)
    write = Column(Boolean, nullable=False, default=False)
    delete = Column(Boolean, nullable=False, default=False)

    group = relationship("Group", back_populates="datasets")
    dataset = relationship("Dataset", back_populates="groups")


class Group(Base, TableNameIdMixin):
    name = Column(String(20), nullable=False)
    users = relationship(
        "User",
        secondary=user_group_associations,
        back_populates="groups")

    datasets = relationship("Dataset_Group_Association", back_populates="group")
