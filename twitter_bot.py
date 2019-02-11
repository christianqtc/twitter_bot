import twitter_creds
import tweepy
import tweepy.streaming as StreamListener


# auth = tweepy.OAuthHandler(twitter_creds.CONSUMER_KEY, twitter_creds.CONSUMER_SECRET)
# auth.set_access_token(twitter_creds.ACCESS_TOKEN, twitter_creds.ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


if __name__ == '__main__':

    #listener = StdOutListener()
    auth = tweepy.OAuthHandler(twitter_creds.CONSUMER_KEY, twitter_creds.CONSUMER_SECRET)
    auth.set_access_token(twitter_creds.ACCESS_TOKEN, twitter_creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    #stream = tweepy.Stream(auth, listener)

    public_tweets = api.home_timeline()

    for tweet in public_tweets:
        print(tweet.user.screen_name, ": ", tweet.text)

    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(api.auth, myStreamListener)
    #
    # myStream.filter(track=['travis jordan'])