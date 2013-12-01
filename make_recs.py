### IMPORT MODULES
import json
import os
import tweepy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction import stop_words
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD


### LOAD TWEET JSON DATA
df = pd.DataFrame()
for tweet_file in os.listdir('tweet_json/'):
    json_data = open('tweet_json/' + tweet_file)
    json_dict = json.load(json_data)
    df = pd.concat([df, pd.DataFrame(json_dict)])

# re-index df
df = df[df.num_tweets >= 10]
df.index = range(len(df))


### PROCESS TWEETS
df['tweet_str'] = df['tweets'].apply(' '.join)


### CREATE TOKEN MATRIX
# vect = CountVectorizer().fit(df.tweet_str)
s_words = stop_words.ENGLISH_STOP_WORDS
vect = TfidfVectorizer(stop_words=s_words).fit(df.tweet_str)
matrix = vect.transform(df.tweet_str)
# reduce feature space with LSA
svd = TruncatedSVD(n_components=100).fit(matrix)
matrix = svd.transform(matrix)


### BUILD RECOMMENDATION ENGINE
nbrs = NearestNeighbors(n_neighbors=20)
nbrs.fit(matrix)


### TAKE IN TWITTER HANDLE AND MAKE RECCOMENDATIONS
auth = tweepy.OAuthHandler('6uhR4asteKqbRZrF58Gg', 'euNYEIYJqkrB2jxRTy3w83VvnNqxEQqfB8DTOvveUc')
auth.set_access_token('1970118768-tUZUlPpMNeMWycB23gkAphGDLzRmjMrI3bfqDdY', 'fyEQQeqp14oRX9cdpYoUNykZfLEEM6Kkozh7QkTiGxHPc')
api = tweepy.API(auth)

while True:
    screen_name = raw_input('\nenter a twitter handle:  ')
    if screen_name == 'q':
        break
    artist_tweets = api.user_timeline(screen_name, count=200)
    tweet_list = [x.text for x in artist_tweets]
    tweet_str = ' '.join(tweet_list)
    tokens = vect.transform([tweet_str])
    tokens = svd.transform(tokens)
    distances, indices = nbrs.kneighbors(tokens)
    artists = [df.screen_name[i] for i in indices[0]]
    for i, artist in enumerate(artists):
        print artist, '  ', distances[0][i]
