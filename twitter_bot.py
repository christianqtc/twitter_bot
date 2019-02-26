import twitter_creds
import tweepy
import csv
import time
import pandas as pd
import tweepy.streaming as StreamListener


# auth = tweepy.OAuthHandler(twitter_creds.CONSUMER_KEY, twitter_creds.CONSUMER_SECRET)
# auth.set_access_token(twitter_creds.ACCESS_TOKEN, twitter_creds.ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


def stream_tweets(api):

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(api.auth, myStreamListener)

    myStream.filter(track=['travis jordan'])


def store_tweets(api):
    tweets = api.search(q="giveaway follow OR win follow OR winner giveaway OR giveaway rt OR giveaway retweet",
                        count=10)
    csvFile = open('test.csv', 'w+', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('time', 'user.id', 'user.screen_name', 'tweet.id', 'text'))
        for tweet in tweets:
            writer.writerow((tweet.created_at, tweet.user.id, tweet.user.screen_name, tweet.id, tweet.text))
    finally:
        csvFile.close()
    return tweets


def get_api():

    auth = tweepy.OAuthHandler(twitter_creds.CONSUMER_KEY, twitter_creds.CONSUMER_SECRET)
    auth.set_access_token(twitter_creds.ACCESS_TOKEN, twitter_creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def search_tweets(api):
    public_tweets = api.home_timeline()

    search_results = api.search(q="giveaway follow OR win follow OR winner giveaway OR giveaway rt OR giveaway retweet "
                                  "AND -filter:retweets", count=1)

    for tweet in search_results:
        print(tweet.user.screen_name, ": ", tweet.text)

    # print(search_results[0])
    # print('\n')
    # print(search_results[0].user.screen_name, ": ", search_results[0].text)


def follow_user_retweet_like(api):
    tweets = store_tweets(api)
    # for tweet in tweets:
    #     api.create_friendship(tweet.user.id)
    #     api.retweet()

    # try:
        # if user_mentions.id in tweets[0]:
        #     api.create_friendship(tweets[0].user_mentions.id)
    for tweet in tweets:
        if tweet.retweeted_status.user.screen_name:
            print("Retweeter person: ", tweet.user.screen_name, " Followed: ",
                  tweet.retweeted_status.user.screen_name, " and Retweeted and Liked: ", tweet.text)
            api.create_friendship(tweet.retweeted_status.user.screen_name)
        else:
            print("Original person: ", tweet.user.screen_name, " Followed: ",
                  tweet.user.screen_name, " and Retweeted and Liked: ", tweet.text)
            api.create_friendship(tweet.user.screen_name)
        api.create_favorite(tweet.id)
        tweet.retweet()
    # except tweepy.TweepError:
    #     print("Rate Limit reached...")
    #     print("...")



if __name__ == '__main__':

    api = get_api()
    store_tweets(api)
    search_tweets(api)
    follow_user_retweet_like(api)

