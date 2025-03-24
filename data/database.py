from sqlalchemy import create_engine, select, insert
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
            insert_stmt = type(obj).insert_stmt(obj)
            session.execute(insert_stmt)
            session.commit()
    
    def create_objects(self, objs, batch=100):
        with Session(self.engine) as session:
            session.add_all(objs)
            session.commit()

    def retrieve_object(self, obj):
        with Session(self.engine) as session:
            stmt = type(obj).select_stmt(obj)
            return session.execute(stmt).scalars().first()
        
    def retrieve_objects(self, type):
        with Session(self.engine) as session:
            stmt = type.select_stmt()
            return session.execute(stmt).scalars().all()