from service.feed_service import FeedService
from data.tables import Group, Content, Subscription, UserSettings
from datetime import datetime
from time import mktime
import util.util as util

class FeedLoader:
    def __init__(self):
        self.feed_service = FeedService()

    def create_user_settings(self):
        self.feed_service.create_user_settings(UserSettings)

    def update_user_settings(self, settings):
        settings.auto_sync = util.validate_boolean('Auto sync feeds? True / False: ')
        settings.volume = util.validate_float('Enter volume from 0 to 1: ', 0, 1)
        settings.display_images = util.validate_boolean('Display images? True or False: ')
        self.feed_service.update_user_settings(UserSettings, settings)
    
    def retrieve_user_settings(self):
        return self.feed_service.retrieve_obj(UserSettings, 'user')

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
    
    
    def list_content(self, subscription):
        content = self.feed_service.retrieve_content(Content, subscription.id)
        return self.paginate_select_content(content, 0, 20 if len(content) >= 20 else len(content))

    def paginate_select_content(self, content, start, end):
        while True:
            [print('{0})'.format(i+1), content[i]) for i in range(start, end)]
            if not end >= len(content) and util.validate_boolean('Next page? y or n: '):
                start = end
                end = end + 20 if end + 20 <= len(content) else len(content)
            else:
                if util.validate_boolean('Want to select an episode? y or n: '):
                    idx = util.validate_int('Select an episode number: ', 0, len(content))
                    return (content[idx - 1], content)
                else: break

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
        subscriptions = self.feed_service.retrieve_objs(Subscription)
        [print('{0}.'.format(i+1), subscriptions[i]) for i in range(0, len(subscriptions))]
        return subscriptions
    
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
        feed = self.retrieve_feed(subscription.feed_url)
        entries = [entry for entry in feed.entries if datetime.fromtimestamp(mktime(entry.published_parsed)) > subscription.last_item_date]
        self.process_feed_entries(subscription, entries)

    def sync_all(self):
        subscriptions = self.feed_service.retrieve_objs(Subscription)
        [self.sync_subscription(subscription.feed_url) for subscription in subscriptions]

    def process_feed_entries(self, subscription, entries):
        content = self.build_content(entries, subscription.group_id, subscription.id)
        self.create_content(Content, content)
        if len(content) > 0: self.update_subscription(subscription, content[0].publish_date)
# https://feeds.acast.com/public/shows/b6085bcd-3542-4a43-b6a8-021e3fd251b8
# https://friendsatthetable.net/rss
