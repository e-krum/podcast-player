from service.feed_loader import FeedLoader
from service.media_service import MediaService
import util.util as util
from pynput.keyboard import Listener

def initiate_settings(feed_loader):
    feed_loader.create_user_settings()
    return feed_loader.retrieve_user_settings()

def update_settings(feed_loader, user_settings):
    feed_loader.update_user_settings(user_settings)

def list_options(feed_loader):
    msg = '''
Select an option from the list below:\n
1. Enter a new feed url
2. Sync a feed url
3. List existing feeds
4. List episodes for a feed 
5. Update user settings
'''
    return util.validate_int(msg, 1, 5)

def process_selection(feed_loader, user_settings, media_service):
    selection = list_options(feed_loader)
    match selection:
        case 1:
            url = input('Enter feed url to subscribe to - ')
            feed_loader.subscribe(url)
        case 2:
            url = input('Enter a feed url to sync - ')
            feed_loader.sync_subscription(url)
        case 3:
            subscriptions = feed_loader.list_subscriptions()
            list_content = util.validate_boolean('Load episodes for a feed, y or n? ')
            if list_content: 
                content_tuple = feed_loader.list_content(subscriptions[util.validate_int('Enter selection: ', 1, len(subscriptions)) - 1])
                if content_tuple is not None:
                    # ask if wish to play the episode
                    if util.validate_boolean('Play selected episode? y or n: '):
                        media_service.play_loop(content_tuple[0])
        case 4:
            pass
        case 5:
            update_settings(feed_loader, user_settings)


def main():
    print('Welcome to your new podcast destination!\n')
    
    feed_loader = FeedLoader()
    user_settings = initiate_settings(feed_loader)
    media_service = MediaService()
    if user_settings.auto_sync: feed_loader.sync_all()
    while True:
        process_selection(feed_loader, user_settings, media_service)


if __name__ == "__main__":
    main()