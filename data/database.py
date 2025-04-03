import itertools
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from data.tables import Base

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
            try:
                upsert_stmt = type(obj).upsert_stmt(obj)
                session.execute(upsert_stmt)
                session.commit()
            except SQLAlchemyError as error:
                print(f'Unable to create objects due to {type(error)}')
    
    def create_objects(self, obj_type, objs, batch_size=100):
        with Session(self.engine) as session:
            try:
                for obj in objs:
                    upsert_stmt = obj_type.upsert_stmt(obj)
                    session.execute(upsert_stmt)
                session.commit()
            except SQLAlchemyError as error:
                print(f'Unable to create objects due to {type(error)}')

    def retrieve_object(self, obj_type, value):
        with Session(self.engine) as session:
            try:
                stmt = obj_type.select_by_value_stmt(value)
                return session.execute(stmt).scalars().first()
            except SQLAlchemyError as error:
                print(f'Unable to create objects due to {type(error)}')
        
    def retrieve_objects(self, obj_type):
        with Session(self.engine) as session:
            stmt = obj_type.select_page_stmt(obj_type)
            return session.execute(stmt).scalars().all()
        
    def retrieve_content(self, obj_type, subscription_id):
        with Session(self.engine) as session:
            stmt = obj_type.select_by_subscription_stmt(subscription_id)
            return session.execute(stmt).scalars().all()
    
    def delete_objs(self, obj_type, value):
        with Session(self.engine) as session:
            stmt = obj_type.delete_stmt(obj_type, value)
            ids = session.execute(stmt).scalars().all()
            # session.commit()
            return ids
        
    def delete_content(self, obj_type, group_id, subscription_id):
        with Session(self.engine) as session:
            stmt = obj_type.delete_by_ids_stmt(group_id, subscription_id)
            session.execute(stmt)
            session.commit()

    def update_content(self, obj_type, content):
        with Session(self.engine) as session:
            stmt = obj_type.update_progress(content)
            session.execute(stmt)
            session.commit()