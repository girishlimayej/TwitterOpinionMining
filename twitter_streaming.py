#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv

#Variables that contains the user credentials to access Twitter API
access_token = "696102173122277378-bubyI66Yk10HX6IergZwz8PMrfxRvZY"
access_token_secret = "nAMcxYLddmAwXQQ6l68jkSjv592TOR8iKp7SKnmTeraQj"
consumer_key = "QecVExtQoGgq9v6U9GRau8mXL"
consumer_secret = "pC71CUoIyJg9mkvp554zdJpEH0XpVSXxKAHy6pChpGaSdqdhum"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print (data)
        #tweet=json.loads(data)
        tweet=parse_tweet(data)
        tweet=extract_content(tweet)
        print(tweet)

        with open('tweets.csv', 'a') as f:
            writer = csv.writer(f, quotechar='"')
            writer.writerow(tweet)

        #print(list(data.keys()))
        #print(data['user']['screen_name'],data['text'])

        return True

    def on_error(self, status):
        print (status)
        return False
# parse data
def parse_tweet(data):

    # load JSON item into a dict
    tweet = json.loads(data)


    # check if tweet is valid
    if 'user' in tweet.keys():

        # parse date
        tweet['CREATED_AT'] =tweet['created_at']
        # classify tweet type based on metadata
        if 'retweeted_status' in tweet:
            tweet['TWEET_TYPE'] = 'retweet'

        elif len(tweet['entities']['user_mentions']) > 0:
            tweet['TWEET_TYPE'] = 'mention'

        else:
            tweet['TWEET_TYPE'] = 'tweet'

        return tweet


def extract_content(tweet):

    content = [tweet['user']['screen_name'],
               tweet['created_at'],
               tweet['TWEET_TYPE'],
               tweet['text'].encode('unicode_escape')]

    return content
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['modi'])