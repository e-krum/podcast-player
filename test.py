from service.feed_service import FeedService
from data.tables import Group, Content

feed_service = FeedService()

feed = feed_service.retrieve_feed('https://feeds.acast.com/public/shows/b6085bcd-3542-4a43-b6a8-021e3fd251b8')

group = Group(name=feed.feed.author)
feed_service.save_obj(group)
group = feed_service.retrieve_group(group.name)
entries = [Content(title=entry.title, url=entry.link) for entry in feed.entries]

print('test')