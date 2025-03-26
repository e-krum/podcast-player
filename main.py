from service.feed_loader import FeedLoader
from data.database import Group

def main():
    print('Welcome to your new podcast destination!\nPlease provide a url to the rss feed you wish to subscribe to!')
    feed_loader = FeedLoader()
    while True:
        try:
            url = input('Enter url - ')
            # feed_loader.subscribe(url)
            groups = feed_loader.retrieve(Group)
            print()
        except:
            print('Invalid url provided / not an rss feed')


if __name__ == "__main__":
    main()