### IMPORT MODULES
import json
import csv
import numpy as np
from pandas import DataFrame
import urllib2
from django.utils.encoding import smart_str
twitter_rate_lim = 180

### GET HOT/RELEVANT ARTISTS FROM ECHO NEST
req_str = ('http://developer.echonest.com/api/v4/artist/top_hottt?'
    'api_key=PGFOUPJMLMTIHEQEX&format=json&results=1000'
    '&bucket=hotttnesss&bucket=id:twitter&start=0')
req = urllib2.Request(req_str)
opener = urllib2.build_opener()
f = opener.open(req)
str_json = f.read()
data_dict = json.loads(str_json)['response']['artists']

# tweak twitter field in dict
for item in data_dict:
    if 'foreign_ids' in item.keys():
        item['foreign_ids'] = item['foreign_ids'][0]['foreign_id'][15:]


### PUT ARTIST DATA IN DATAFRAME
df = DataFrame(data_dict)
df.columns = ['screen_name', 'hotttnesss', 'id', 'artist']


### CSV OUTPUT
# handle utf-8 issue for CSV files
df_csv = df
df_csv['artist'] = df_csv['artist'].apply(smart_str)
df_csv.to_csv('artists_hott.csv')


### JSON OUTPUT
df = df.dropna()

# split output into chunks of 180 artists for Twitters rate limit
df_splits = np.array_split(df, len(df)/twitter_rate_lim +1)
for i, split in enumerate(df_splits):
    output_dict = {'artist' : split['artist'].tolist(), 'screen_name' : split['screen_name'].tolist(),
                'hotttnesss' : split['hotttnesss'].tolist()}

    f = open('artist_json/artists_hott' + str(i) + '.json', 'w')
    f.write( json.dumps(output_dict) )





