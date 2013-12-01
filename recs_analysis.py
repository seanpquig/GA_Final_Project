### IMPORT MODULES
import json
from django.utils.encoding import smart_str
import os
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
matrix = TruncatedSVD(n_components=100).fit_transform(matrix)


### BUILD RECOMMENDATION ENGINE
nbrs = NearestNeighbors(n_neighbors=20)
nbrs.fit(matrix)


### CREATE CSV OF ALL RECOMMENDATIONS
recs = []
scores = []
for i, row in enumerate(matrix):
    print i
    distances, indices = nbrs.kneighbors(row)
    # distances, indices = nbrs.kneighbors(row.toarray())
    artists = [df.artist[i] for i in indices[0]]
    recs.append(artists)
    scores.append(distances[0])

df['recommendations'] = recs
df['scores'] = scores
df['artist'] = df['artist'].apply(smart_str)
df[['artist', 'screen_name', 'hotttnesss', 
    'num_tweets', 'recommendations', 'scores']].to_csv('recommendations/recs_LSA_100.csv')



