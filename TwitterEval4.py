
# coding: utf-8

# In[440]:

import pandas as pd


# In[441]:

import numpy as np


# In[442]:

import re


# In[443]:

import matplotlib.pyplot as plt


# In[444]:

from collections import Counter


# In[445]:

import json


# In[446]:

import csv


# In[447]:

get_ipython().magic('matplotlib inline')


# In[448]:

# None for universal newline mode
#df = pd.read_csv(open('twitter-data4.csv',newline = None))

content = open("twitter-data3.csv", "r").read()
content = re.sub('\r', '', content)
with open("1.csv", "w") as g:
    g.write(content)
df = pd.read_csv('digifest2016dataset.csv')


# In[449]:

#df.ix[1807]


# In[450]:

#for x in range(0,10000):
#    print(x, df.ix[x]['entities_str'], source_name(df.ix[x]['entities_str']))


# In[451]:

#for i in range (4000,8000):
#    print(df.ix[i]['geo_coordinates'])


# In[452]:

df = pd.DataFrame.drop_duplicates(df)


# In[453]:

# ADD MORE HANDLING FOR MISSING DATA WHEN ADDING FIELDS


# In[454]:

def is_retweet(s):
    match = re.search("^RT @",s)
    if match == None:
        return False
    else: 
        return True


# In[455]:

def is_reply(s):
    if pd.isnull(s):
        return False
    else: 
        return True


# In[456]:

def source_name(s):
    if pd.isnull(s):
        return np.nan
    
    match = re.search(">((?:\w\s?)+)</a>$",s)
    if match == None:
        return np.nan
    else:
        return match.group(1)


# In[457]:

def get_hashtags(s):
    if pd.isnull(s):
        return np.nan
    
    return_list = []
    json_line = json.loads(s)
    for x in json_line['hashtags']:
        return_list.append(x['text'])
    
    return return_list
    
    #match = re.findall("\"text\":\"([^\"]+)\"",s)
    #return match


# In[458]:

def get_mentions(s):
    if pd.isnull(s):
        return np.nan
    
    return_list = []
    json_line = json.loads(s)
    for x in json_line['user_mentions']:
        return_list.append(x['screen_name'])
                       
    return return_list
    #match = re.findall("\"screen_name\":\"([^\"]+)\"",s)
    #return match


# In[459]:

def get_retweeted(s):
    match = re.search("^RT @([^:]+):",s)
    if match == None:
        return np.nan
    else:
        return match.group(1)


# In[460]:

def tweet_type(r):
    if is_reply(r['in_reply_to_screen_name']):
        return "reply"
    elif is_retweet(r['text']):
        return "retweet"
    else:
        return "tweet"


# In[461]:

df['is_retweet'] = df['text'].map(is_retweet)


# In[462]:

df['is_reply'] = df['in_reply_to_screen_name'].map(is_reply)


# In[463]:

df['source_name'] = df['source'].map(source_name)


# In[464]:

df['hashtags'] = df['entities_str'].map(get_hashtags)


# In[465]:

df['user_mentions'] = df['entities_str'].map(get_mentions)


# In[466]:

df['retweeted_user'] = df['text'].map(get_retweeted)


# In[467]:

df['tweet_type'] = df.apply(lambda row: tweet_type (row), axis = 1)


# In[468]:

#df.ix[454]['entities_str']


# In[469]:

#for x in range(0,10000):
 #   if x != 453:
#        if df.ix[x]['hashtags'] is np.nan:
  #          print(df.ix[x]['entities_str'], x)


# In[470]:

df


# In[471]:

df.to_csv('somewhat_refined.csv', index = False)


# In[472]:

dfr = pd.read_csv('somewhat_refined.csv')


# In[473]:

sources = dfr['source_name'].value_counts()


# In[474]:

sources.max()


# In[475]:

# change to scale on size of dataset
other_total = sources.select(lambda label: sources[label] < sources.max()/10).sum()
sources = sources.select(lambda label: sources[label] >= sources.max()/10)
sources['Other'] = other_total


# In[476]:

source_plot = sources.plot(kind="pie", title = "Applications used for posting on twitter")
source_plot.set_ylabel('')


# In[477]:

type(dfr['source_name'].value_counts())


# In[478]:

tweet_type_pie = dfr['tweet_type'].value_counts().plot(kind = 'pie', 
                                                       title = 'Distribution of types of tweets'
                                                      )
tweet_type_pie.set_ylabel('')


# In[479]:

typegroup = dfr.groupby(['tweet_type', 'from_user'])


# In[480]:

refinedtg = typegroup.size().reset_index()


# In[481]:

refinedtg.rename(columns = {0:'Number'}, inplace = True)


# In[482]:

replies = refinedtg.loc[refinedtg['tweet_type'] == 'reply']


# In[483]:

retweets = refinedtg.loc[refinedtg['tweet_type'] == 'retweet']


# In[484]:

tweets = refinedtg.loc[refinedtg['tweet_type'] == 'tweet']


# In[485]:

rpmean = replies.mean(0, 'Number')['Number']


# In[486]:

rtmean = retweets.mean(0, 'Number')['Number']


# In[487]:

tmean = tweets.mean(0, 'Nuumber')['Number']


# In[488]:

rpstd = replies.std(0, 'Number')['Number']


# In[489]:

rtstd = retweets.std(0, 'Number')['Number']


# In[490]:

tstd = tweets.std(0, 'Number')['Number']


# In[491]:

tweetdict = {'Mean per user':{'Tweets':tmean, 'Retweets':rtmean, 'Replies':rpmean},
             'Standard deviation per user':{'Tweets':tstd, 'Retweets':rtstd, 'Replies':rpstd}}


# In[492]:

typeinfo = pd.DataFrame.from_dict(tweetdict)


# In[493]:

typeinfo


# In[494]:

retweeted = dfr['retweeted_user'].value_counts()


# In[495]:

replied = dfr['in_reply_to_screen_name'].value_counts()


# In[496]:

responsedict = {'Mean':{'Times retweeted(only including users retweeted at least once)'
                        :retweeted.mean(), 
                        'Times replied(only including users replied to at least once)'
                        :replied.mean()},
                'Standard deviation':{'Times retweeted(only including users retweeted at least once)'
                                      :retweeted.std(),
                                      'Times replied(only including users replied to at least once)'
                                      :replied.std()}}


# In[497]:

responseinfo = pd.DataFrame.from_dict(responsedict)


# In[498]:

responseinfo


# In[ ]:




# In[ ]:




# In[ ]:



