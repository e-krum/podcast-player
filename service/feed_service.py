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
    
    def retrieve_group(self, id):
        return self.database.retrieve_group(id)