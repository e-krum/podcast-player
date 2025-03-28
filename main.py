from service.feed_loader import FeedLoader

def main():
    print('Welcome to your new podcast destination!\nPlease provide a url to the rss feed you wish to subscribe to!')
    feed_loader = FeedLoader()
    while True:
        try:
            url = input('Enter url - ')
            # feed_loader.subscribe(url)
            feed_loader.sync_subscription(url)
            print()
        except:
            print('Invalid url provided / not an rss feed')


if __name__ == "__main__":
    main()