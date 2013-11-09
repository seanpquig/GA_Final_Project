### IMPORT MODULES
import json
import csv
import pandas as pd
import tweepy

file_num = 0

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
    artist_tweets = api.user_timeline(screen_name, count=200)
    print screen_name, '  ', len(artist_tweets)
    tweet_list = [x.text for x in artist_tweets]
    return tweet_list

df['tweets'] = df['screen_name'].apply(get_tweets)
df['num_tweets'] = df['tweets'].apply(len)


### JSON OUTPUT
output_dict = {'artist' : df['artist'].tolist(), 'screen_name' : df['screen_name'].tolist(),
            'hotttnesss' : df['hotttnesss'].tolist(), 'num_tweets' : df['num_tweets'].tolist(),
            'tweets' : df['tweets'].tolist() }

f = open('tweet_json/tweets' + str(file_num) + '.json', 'w')
f.write( json.dumps(output_dict) )








# tweet_series = []
# for index, row in df.iterrows():
#     artist_tweets = api.user_timeline(screen_name = row[0], count=200)
#     tweet_concat = ''
#     for tweet in artist_tweets:
#         tweet_concat = tweet_concat + tweet.text + ' ' 
#     tweet_series = tweet_series + [tweet_concat]

# df['tweets'] = tweet_series
