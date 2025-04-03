from service.feed_service import FeedService
from data.tables import Group, Content, Subscription
from datetime import datetime
from time import mktime
# import ffmpeg

class FeedLoader:
    def __init__(self):
        self.feed_service = FeedService()

    def retrieve_feed(self, url):
        return self.feed_service.retrieve_feed(url)
    
    def create_group(self, name):
        try:
            group = Group(name=name)
            self.feed_service.save_obj(group)
            return self.feed_service.retrieve_obj(Group, group.name)
        except:
            return None
    
    def create_subscription(self, title, group, link):
        try:
            subscription = Subscription(title=title, group_id=group.id, feed_url=link.href)
            self.feed_service.save_obj(subscription)
            return self.feed_service.retrieve_obj(Subscription, link.href)
        except Exception as error:
            return None

    def create_content(self, obj_type, entries):
        try:
            self.feed_service.save_objs(obj_type, entries)
        except:
            print('Error occurred while attempting to save content')
    
    def build_content(self, entries, group_id, subscription_id):
        content = list()
        for entry in entries:
            url = next(link.href for link in entry.links if link.type.startswith('audio'))
            # length = ffmpeg.probe(url)['format']['duration']
            publish_date = datetime.fromtimestamp(mktime(entry.published_parsed))
            content.append(Content(group_id=group_id, subscription_id=subscription_id, title=entry.title, publish_date=publish_date, url=url, finished=False))
        content.sort(key=Content.sort, reverse=True)
        return content
    
    def subscribe(self, url):
        feed = self.retrieve_feed(url)
        if False == feed.bozo:
            group = self.create_group(feed.feed.author)
            if group is not None:
                link = next(item for item in feed.feed.links if item['rel'] == 'self')
                subscription = self.create_subscription(feed.feed.title, group, link)
                if subscription is not None:
                    self.process_feed_entries(subscription, feed.entries)
    
    def list_subscriptions(self):
        return self.feed_service.retrieve_objs(Subscription)
    
    def unsubscribe(self, url):
        # remove subscription from table
        ids = self.feed_service.delete_objs(Subscription, url)
        # remove all content tied to subscription
        self.feed_service.delete_content(Content, ids.group_id, ids.subscription_id)

    # update last entry in subscription
    def update_subscription(self, subscription, publish_date):
        subscription.last_item_date = publish_date
        self.feed_service.save_obj(subscription)

    def sync_subscription(self, url):
        # take passed in id and check for new content from feed url
        subscription = self.feed_service.retrieve_obj(Subscription, url)
        feed = self.feed_service.retrieve_feed(subscription.feed_url)
        entries = [entry for entry in feed.entries if datetime.fromtimestamp(mktime(entry.published_parsed)) > subscription.last_item_date]
        self.process_feed_entries(subscription, entries)
        pass

    def process_feed_entries(self, subscription, entries):
        content = self.build_content(entries, subscription.group_id, subscription.id)
        self.create_content(Content, content)
        self.update_subscription(subscription, content[0].publish_date)
# https://feeds.acast.com/public/shows/b6085bcd-3542-4a43-b6a8-021e3fd251b8
# https://friendsatthetable.net/rss
