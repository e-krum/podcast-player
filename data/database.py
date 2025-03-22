from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from data.tables import Base, Group, Content, PlayedContent, Subscription

class Database():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.engine = create_engine('sqlite:///podcast.db')
        self.base = Base
        self.create_tables()

    def create_tables(self):
        self.base.metadata.create_all(self.engine)

    def create_object(self, obj):
        with Session(self.engine) as session:
            session.add(obj)
            session.commit()
    
    def create_objects(self, objs):
        with Session(self.engine) as session:
            session.add_all(objs)
            session.commit()

    def retrieve_group(self, name):
        with Session(self.engine) as session:
            stmt = select(Group).where(Group.name.match(name))
            return session.scalar(stmt)