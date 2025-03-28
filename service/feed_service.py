import feedparser
from data.database import Database

class FeedService:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FeedService, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.database = Database()

    def retrieve_feed(self, url):
        return feedparser.parse(url)

    def save_obj(self, obj):
        self.database.create_object(obj)

    def save_objs(self, obj_type, objs):
        self.database.create_objects(obj_type, objs)
    
    def retrieve_obj(self, obj_type, value):
        return self.database.retrieve_object(obj_type, value)
    
    def retrieve_objs(self, obj_type):
        return self.database.retrieve_objects(obj_type)
    
    def retrieve_content(self, obj_type, subscription_id):
        return self.database.retrieve_content(obj_type, subscription_id)