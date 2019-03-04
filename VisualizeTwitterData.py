import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap

#tweets = []
mental_f = 'mental.json'
mental_f2 = 'mental2.json'
anxiety_f ='anxiety.json'
anxiety_f2 ='anxiety2.json'
bipolar_f = 'bipolar.json'
bipolar_f2 = 'bipolar2.json'
bts_f = 'bts.json'
bts_f2 = 'bts2.json'
dep_f = 'depression.json'
dep_f2 = 'depression2.json'
na_f = 'na.json'
na_f2 = 'na2.json'
panic_f = 'panic.json'
panic_f2 = 'panic2.json'

tweet_files_1 = [mental_f, mental_f2, anxiety_f, anxiety_f2, bipolar_f, bipolar_f2, dep_f, dep_f2, panic_f, panic_f2]
grouped_tweet = []
for file in tweet_files_1:
    with open(file, 'r') as f:
        for line in f.readlines():
            grouped_tweet.append(json.loads(line))

tweet_bts = [bts_f, bts_f2]
grouped_bts = []
for file in tweet_bts:
    with open(file,'r') as f:
        for line in f.readlines():
            grouped_bts.append(json.loads(line))

tweet_na = [na_f, na_f2]
grouped_na = []
for file in tweet_na:
    with open(file,'r') as f:
        for line in f.readlines():
            grouped_na.append(json.loads(line))

def populate_tweet_df(tweets):
    df = pd.DataFrame()

    df['text'] = list(map(lambda tweet: tweet['text'], tweets))

    df['location'] = list(map(lambda tweet: tweet['user']['location'], tweets))

    df['country_code'] = list(map(lambda tweet: tweet['place']['country_code']
                                  if tweet['place'] != None else '', tweets))

    df['long'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][0]
                        if tweet['coordinates'] != None else 'NaN', tweets))

    df['latt'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][1]
                        if tweet['coordinates'] != None else 'NaN', tweets))

    return df


df_group = populate_tweet_df(grouped_tweet)
df_bts = populate_tweet_df(grouped_bts)
df_na = populate_tweet_df(grouped_na)
# Size of the map
fig = plt.figure(figsize=(18, 4), dpi=250)
# Set a title
plt.title("Mental Health Related Tweets: A Worldwide Survey ")
# plot the blank world map
my_map = Basemap(projection='merc',
              llcrnrlat=-80,
              urcrnrlat=80,
              llcrnrlon=-180,
              urcrnrlon=180,
              lat_ts=20)
# set resolution='h' for high quality
my_map.shadedrelief(scale=0.5)

# add coordinates as red dots
longs_1 = list(df_group.loc[(df_group.long != 'NaN')].long)
latts_1 = list(df_group.loc[df_group.latt != 'NaN'].latt)
x1, y1 = my_map(longs_1, latts_1)
plt.plot(x1, y1, 'ro', markersize=2, alpha=0.5)

# add coordinates as blue dots
longs_bts = list(df_bts.loc[(df_bts.long != 'NaN')].long)
latts_bts = list(df_bts.loc[df_bts.latt != 'NaN'].latt)
x_bts, y_bts = my_map(longs_bts, latts_bts)
plt.plot(x_bts, y_bts, 'bo', markersize=2, alpha=0.5)

# add coordinates as green triangles
longs_na = list(df_na.loc[(df_na.long != 'NaN')].long)
latts_na = list(df_na.loc[df_na.latt != 'NaN'].latt)
x_na, y_na = my_map(longs_na, latts_na)
plt.plot(x_na, y_na, 'g^', markersize=2, alpha=0.5)

plt.savefig('output.png', pad_inches=0.0, bbox_inches='tight')

#df_group_cleaned = df_group[['long','latt']]
#test_list = [list(l) for l in zip(longs_1, latts_1)]
#test_np_list = np.array(test_list)
#np.savetxt('output.csv', test_np_list, delimiter=',', header='')
#plt.show()
