
# coding: utf-8

# In[78]:

import pandas as pd


# In[79]:

import numpy as np


# In[80]:

import re


# In[81]:

import matplotlib.pyplot as plt


# In[82]:

from collections import Counter


# In[83]:

import json


# In[84]:

import csv


# In[85]:

get_ipython().magic('matplotlib inline')


# In[86]:

df = pd.read_csv('digifest2016dataset.csv')


# In[87]:

def is_retweet(s):
    """Determines whether a tweet is a retweet"""
    
    # Match retweet in text and return True/ False if matched/not matched
    match = re.search('^RT @',s)
    if match == None:
        return False
    else: 
        return True


# In[88]:

def is_reply(s):
    """Determines whether a tweet is a reply"""
    
    if pd.isnull(s):
        return False
    else: 
        return True


# In[89]:

def source_name(s):
    """Finds the name of the application used for tweeting"""
    
    # Return NaN if there is no source name in data
    if pd.isnull(s):
        return np.nan
    
    # Find source name in url and return it if found and NaN otherwise
    match = re.search('>((?:\w\s?)+)</a>$',s)
    if match == None:
        return np.nan
    else:
        return match.group(1)


# In[90]:

def get_hashtags(s):
    """Gets a list of hashtags in a tweet"""
    
    return_list = []
    json_line = json.loads(s)
    
    # Append each hashtag to list of hashtags to return
    for x in json_line['hashtags']:
        return_list.append(x['text'])
    
    return return_list


# In[91]:

def get_mentions(s):
    """Gets a list of mentioned users in a tweet"""
    
    return_list = []
    json_line = json.loads(s)
    
    # Append each user mentioned to list to return
    for x in json_line['user_mentions']:
        return_list.append(x['screen_name'])
                       
    return return_list


# In[92]:

def get_retweeted(s):
    """Gets retweeted user in a retweet"""
    
    # Match user that was retweeted and return it or NaN if no match
    match = re.search("^RT @([^:]+):",s)
    if match == None:
        return np.nan
    else:
        return [match.group(1)]


# In[93]:

def tweet_type(r):
    """Gets the type of tweet a row represents"""
    
    # Check for each tweet type and returns appropriate value
    if is_reply(r['in_reply_to_screen_name']):
        return "reply"
    elif is_retweet(r['text']):
        return "retweet"
    else:
        return "tweet"


# In[94]:

def to_list(s):
    """converts a value to a list if it is not null"""
    
    # Return NaN if s is empty or s as list otherwise
    if pd.isnull(s):
        return np.nan
    else:
        return [s]


# In[95]:

df['is_retweet'] = df['text'].map(is_retweet)


# In[96]:

df['is_reply'] = df['in_reply_to_screen_name'].map(is_reply)


# In[97]:

df['source_name'] = df['source'].map(source_name)


# In[98]:

df['hashtags'] = df['entities_str'].map(get_hashtags)


# In[99]:

df['user_mentions'] = df['entities_str'].map(get_mentions)


# In[100]:

df['retweeted_user'] = df['text'].map(get_retweeted)


# In[101]:

df['replied_to_user'] = df['in_reply_to_screen_name'].map(to_list)


# In[102]:

df['tweet_type'] = df.apply(lambda row: tweet_type (row), axis = 1)


# In[103]:

df


# In[104]:

df.to_csv('somewhat_refined.csv', index = False)


# In[105]:

dfr = pd.read_csv('somewhat_refined.csv', lineterminator = '\n')


# In[106]:

sources = dfr['source_name'].value_counts()


# In[108]:

# size of other scalse with dataset size
other_total = sources.select(lambda label: sources[label] < sources.max()/12).sum()
sources = sources.select(lambda label: sources[label] >= sources.max()/12)
sources['Other'] = other_total


# In[109]:

source_plot = sources.plot(kind="pie", 
                           title = "Applications used for posting on twitter",
                          )
source_plot.set_ylabel('')


# In[111]:

tweet_type_pie = dfr['tweet_type'].value_counts().plot(kind = 'pie', 
                                                       title = 'Distribution of types of tweets'
                                                      )
tweet_type_pie.set_ylabel('')


# In[112]:

typegroup = dfr.groupby(['tweet_type', 'from_user'])


# In[113]:

refinedtg = typegroup.size().reset_index()


# In[114]:

refinedtg.rename(columns = {0:'Number'}, inplace = True)


# In[115]:

replies = refinedtg.loc[refinedtg['tweet_type'] == 'reply']


# In[116]:

retweets = refinedtg.loc[refinedtg['tweet_type'] == 'retweet']


# In[117]:

tweets = refinedtg.loc[refinedtg['tweet_type'] == 'tweet']


# In[118]:

rpmean = replies.mean(0, 'Number')['Number']


# In[119]:

rtmean = retweets.mean(0, 'Number')['Number']


# In[120]:

tmean = tweets.mean(0, 'Nuumber')['Number']


# In[121]:

rpstd = replies.std(0, 'Number')['Number']


# In[122]:

rtstd = retweets.std(0, 'Number')['Number']


# In[123]:

tstd = tweets.std(0, 'Number')['Number']


# In[124]:

tweetdict = {'Mean per user':{'Tweets':tmean, 'Retweets':rtmean, 'Replies':rpmean},
             'Standard deviation per user':{'Tweets':tstd, 'Retweets':rtstd, 'Replies':rpstd}}


# In[125]:

typeinfo = pd.DataFrame.from_dict(tweetdict)


# In[126]:

typeinfo


# In[127]:

retweeted = dfr['retweeted_user'].value_counts()


# In[128]:

replied = dfr['in_reply_to_screen_name'].value_counts()


# In[129]:

responsedict = {'Mean':{'Times retweeted(only including users retweeted at least once)'
                        :retweeted.mean(), 
                        'Times replied(only including users replied to at least once)'
                        :replied.mean()},
                'Standard deviation':{'Times retweeted(only including users retweeted at least once)'
                                      :retweeted.std(),
                                      'Times replied(only including users replied to at least once)'
                                      :replied.std()}}


# In[130]:

responseinfo = pd.DataFrame.from_dict(responsedict)


# In[131]:

responseinfo


# In[ ]:




# In[ ]:




# In[ ]:



