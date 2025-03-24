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
    
    def create_subscription(self, group, link):
        subscription = Subscription(title=group.title, group_id=group.id, feed_url=link.href)
        self.feed_service.save_obj(subscription)

    def create_content(self, entries):
        self.feed_service.save_objs(entries)
    
    def subscribe(self, url):
        feed = self.retrieve_feed(url)
        group = self.create_group(feed.feed.author)
        # link = next(item for item in feed.feed.links if item['rel'] == 'self')
        # self.create_subscription(group, link)
        # self.create_content([Content(group_id=group.id, title=entry.title, url=entry.link, publish_date=entry.published) for entry in feed.entries])
    
    def list_subscriptions(self):
        return self.feed_service.retrieve_objs(Subscription)
    
    def unsubscribe(self, id):
        # remove subscription from table
        # remove all content tied to subscription
        # remove all played content (gather list of ids of removed content)
        pass

# https://feeds.acast.com/public/shows/b6085bcd-3542-4a43-b6a8-021e3fd251b8
# https://friendsatthetable.net/rss
