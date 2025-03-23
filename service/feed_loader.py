from service.feed_service import FeedService
from data.tables import Group, Content, Subscription


class FeedLoader:
    def __init__(self):
        self.feed_service = FeedService()

    def retrieve_feed(self, url):
        return self.feed_service.retrieve_feed(url)
    
    def create_group(self, name):
        group = Group(name=name)
        self.feed_service.save_obj(group)
        return self.feed_service.retrieve_obj(group)
    
    def build_subscription(self, group, link):
        return Subscription(title=group.title, group_id=group.id, feed_url=link.href)
    
    def subscribe(self, url):
        feed = self.retrieve_feed(url)
        group = self.create_group(feed.feed.author)
        link = next(item for item in feed.feed.links if item['rel'] == 'self')
        subscription = feed_loader.build_subscription(group, link)
        entries = [Content(group_id=group.id, title=entry.title, url=entry.link, publish_date=entry.published) for entry in feed.entries]

# https://feeds.acast.com/public/shows/b6085bcd-3542-4a43-b6a8-021e3fd251b8
# https://friendsatthetable.net/rss
