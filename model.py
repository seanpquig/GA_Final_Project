### IMPORT MODULES
import json
import csv
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


df = pd.DataFrame()
### LOAD TWEET JSON DATA
for tweet_file in os.listdir('tweet_json/'):
    json_data = open('tweet_json/' + tweet_file)
    json_dict = json.load(json_data)
    df = pd.concat([df, pd.DataFrame(json_dict)])


def combine_tweets(tweets):
    tweet_str = ''
    for tweet in tweets:
        tweet_str += (tweet + ' ')
    return tweet_str

df['tweet_str'] = df['tweets'].apply(combine_tweets)

vectorizer = CountVectorizer().fit(df.tweet_str)
tfidf_vect = TfidfVectorizer().fit(df.tweet_str)
matrix = vectorizer.transform(df.tweet_str)
tfidf_matrix = tfidf_vect.transform(df.tweet_str)


nbrs = NearestNeighbors(n_neighbors=10).fit(matrix)
tfidf_nbrs = NearestNeighbors(n_neighbors=10).fit(tfidf_matrix)
distances, indices = nbrs.kneighbors(matrix[0])




