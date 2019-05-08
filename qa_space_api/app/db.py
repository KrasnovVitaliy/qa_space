import datetime
from sqlalchemy import create_engine, Column, DateTime, Integer, String, func, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Config

config = Config()

Base = declarative_base()

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(config.DB_URI))
session = scoped_session(Session)


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(50))
    description = Column(String(100))
    creator = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, name=None, creator=None, description=None):
        self.name = name
        self.description = description
        self.creator = creator

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', 'description', 'creator', 'deleted']
        return self.serialize(to_serialize)


class Suites(Base):
    __tablename__ = 'suites'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(50))
    description = Column(String(100))
    creator = Column(Integer)
    project = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, name=None, creator=None, project=None, description=None):
        self.name = name
        self.creator = creator
        self.project = project
        self.description = description

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', 'description', 'creator', 'project', 'deleted']
        return self.serialize(to_serialize)


class Cases(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(50))
    description = Column(String(100))
    creator = Column(Integer)
    suite = Column(Integer)
    priority = Column(String(10))
    case_type = Column(String(15))
    behaviour = Column(String(15))
    preconditions = Column(String(100))
    postconditions = Column(String(100))
    deleted = Column(DateTime)

    def __init__(self, name=None, creator=None, description=None, suite=None, priority=None,
                 case_type=None, behaviour=None, preconditions=None, postconditions=None):
        self.name = name
        self.creator = creator
        self.description = description
        self.suite = suite
        self.priority = priority
        self.case_type = case_type
        self.behaviour = behaviour
        self.preconditions = preconditions
        self.postconditions = postconditions

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', "description", 'creator', 'suite',
                        'priority', 'case_type', 'behaviour', 'preconditions', 'postconditions', 'deleted']
        return self.serialize(to_serialize)


class Steps(Base):
    __tablename__ = 'steps'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    position = Column(Integer)
    description = Column(String(200))
    creator = Column(Integer)
    case = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, position=None, creator=None, description=None, suite=None, deleted=None):
        self.position = position
        self.creator = creator
        self.description = description
        self.suite = suite
        self.deleted = deleted

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'position', "description", 'creator', 'case']
        return self.serialize(to_serialize)


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(100), unique=True)
    creator = Column(Integer)
    deleted = Column(DateTime)

    def __init__(self, name=None, creator=None, deleted=None):
        self.name = name
        self.creator = creator
        self.deleted = deleted

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'name', 'creator']
        return self.serialize(to_serialize)


class CasesTagsRelation(Base):
    __tablename__ = 'cases_tags_relation'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    case = Column(Integer)
    tag = Column(Integer)

    def __init__(self, case=None, tag=None):
        self.case = case
        self.tag = tag

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'update_date', 'case', 'tag']
        return self.serialize(to_serialize)


def prepare_db():
    engine = create_engine(config.DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# creates database
if __name__ == "__main__":
    prepare_db()
