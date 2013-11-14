### IMPORT MODULES
import json
import csv
import pandas as pd
import twitter

CONSUMER_KEY = '6uhR4asteKqbRZrF58Gg'
CONSUMER_SECRET = 'euNYEIYJqkrB2jxRTy3w83VvnNqxEQqfB8DTOvveUc'
OAUTH_TOKEN = '1970118768-tUZUlPpMNeMWycB23gkAphGDLzRmjMrI3bfqDdY'
OAUTH_TOKEN_SECRET = 'fyEQQeqp14oRX9cdpYoUNykZfLEEM6Kkozh7QkTiGxHPc'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, 
                            CONSUMER_KEY, CONSUMER_SECRET)

api = twitter.Twitter(auth=auth)



file_num = 2

### LOAD ECHO NEST JSON DATA
json_data = open('artist_json/artists_hott' + str(file_num) + '.json')
json_dict = json.load(json_data)
df = pd.DataFrame(json_dict)


### GET TWEETS FOR ARTISTS
# Twitter OAuth 
auth = tweepy.OAuthHandler('6uhR4asteKqbRZrF58Gg', 'euNYEIYJqkrB2jxRTy3w83VvnNqxEQqfB8DTOvveUc')
auth.set_access_token('1970118768-tUZUlPpMNeMWycB23gkAphGDLzRmjMrI3bfqDdY', 'fyEQQeqp14oRX9cdpYoUNykZfLEEM6Kkozh7QkTiGxHPc')

api = tweepy.API(auth)


def get_tweets(screen_name):
    try:
        artist_tweets = api.user_timeline(screen_name, count=200)
    except tweepy.error.TweepError:
        print '******TweepError for:  ', screen_name
        return []
    else:
        tweet_list = [x.text for x in artist_tweets]
        print screen_name, '  ', len(tweet_list)
        return tweet_list


df['tweets'] = df['screen_name'].apply(get_tweets)
df['num_tweets'] = df['tweets'].apply(len)


### JSON OUTPUT
output_dict = {'artist' : df['artist'].tolist(), 'screen_name' : df['screen_name'].tolist(),
            'hotttnesss' : df['hotttnesss'].tolist(), 'num_tweets' : df['num_tweets'].tolist(),
            'tweets' : df['tweets'].tolist() }

f = open('tweet_json/tweets' + str(file_num) + '.json', 'w')
f.write( json.dumps(output_dict) )
