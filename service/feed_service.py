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

    def save_objs(self, objs):
        self.database.create_objects(objs)
    
    def retrieve_obj(self, obj):
        return self.database.retrieve_object(obj)
    
    def retrieve_obj(self, type):
        return self.database.retrieve_objects(type)