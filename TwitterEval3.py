
# coding: utf-8

# In[914]:

import pandas as pd


# In[915]:

import numpy as np


# In[916]:

import re


# In[917]:

import matplotlib.pyplot as plt


# In[918]:

from collections import Counter


# In[919]:

get_ipython().magic('matplotlib inline')


# In[920]:

df = pd.read_csv('digifest2016dataset.csv')


# In[921]:

df = pd.DataFrame.drop_duplicates(df)


# In[922]:

def is_retweet(s):
    match = re.search("^RT @",s)
    if match == None:
        return False
    else: 
        return True


# In[923]:

def is_reply(s):
    if pd.isnull(s):
        return False
    else: 
        return True


# In[924]:

def source_name(s):
    match = re.search(">((?:\w\s?)+)</a>$",s)
    if match == None:
        return "No source found"
    else:
        return match.group(1)


# In[925]:

def get_hashtags(s):
    match = re.findall("\"text\":\"([^\"]+)\"",s)
    return match


# In[926]:

def get_mentions(s):
    match = re.findall("\"screen_name\":\"([^\"]+)\"",s)
    return match


# In[927]:

def get_retweeted(s):
    match = re.search("^RT @([^:]+):",s)
    if match == None:
        return np.nan
    else:
        return match.group(1)


# In[928]:

def tweet_type(r):
    if is_reply(r['in_reply_to_screen_name']):
        return "reply"
    elif is_retweet(r['text']):
        return "retweet"
    else:
        return "tweet"


# In[929]:

df['is_retweet'] = df['text'].map(is_retweet)


# In[930]:

df['is_reply'] = df['in_reply_to_screen_name'].map(is_reply)


# In[931]:

df['source_name'] = df['source'].map(source_name)


# In[932]:

df['hashtags'] = df['entities_str'].map(get_hashtags)


# In[933]:

df['user_mentions'] = df['entities_str'].map(get_mentions)


# In[934]:

df['retweeted_user'] = df['text'].map(get_retweeted)


# In[935]:

df['tweet_type'] = df.apply(lambda row: tweet_type (row), axis = 1)


# In[936]:

df


# In[937]:

df.to_csv('somewhat_refined.csv', index = False)


# In[938]:

dfr = pd.read_csv('somewhat_refined.csv')


# In[939]:

sources = dfr['source_name'].value_counts()


# In[940]:

other_total = sources.select(lambda label: sources[label] < 200).sum()
sources = sources.select(lambda label: sources[label] >= 200)
sources['Other'] = other_total


# In[941]:

source_plot = sources.plot(kind="pie", title = "Applications used for posting on twitter")
source_plot.set_ylabel('')


# In[942]:

type(dfr['source_name'].value_counts())


# In[943]:

tweet_type_pie = dfr['tweet_type'].value_counts().plot(kind = 'pie', 
                                                       title = 'Distribution of types of tweets'
                                                      )
tweet_type_pie.set_ylabel('')


# In[944]:

typegroup = dfr.groupby(['tweet_type', 'from_user'])


# In[945]:

refinedtg = typegroup.size().reset_index()


# In[946]:

refinedtg.rename(columns = {0:'Number'}, inplace = True)


# In[947]:

replies = refinedtg.loc[ss3['tweet_type'] == 'reply']


# In[948]:

retweets = refinedtg.loc[ss3['tweet_type'] == 'retweet']


# In[949]:

tweets = refinedtg.loc[ss3['tweet_type'] == 'tweet']


# In[950]:

rpmean = replies.mean(0, 'Number')['Number']


# In[951]:

rtmean = retweets.mean(0, 'Number')['Number']


# In[952]:

tmean = tweets.mean(0, 'Nuumber')['Number']


# In[953]:

rpstd = replies.std(0, 'Number')['Number']


# In[954]:

rtstd = retweets.std(0, 'Number')['Number']


# In[955]:

tstd = tweets.std(0, 'Number')['Number']


# In[956]:

tweetdict = {'Mean per user':{'Tweets':tmean, 'Retweets':rtmean, 'Replies':rpmean},
             'Standard deviation per user':{'Tweets':tstd, 'Retweets':rtstd, 'Replies':rpstd}}


# In[957]:

typeinfo = pd.DataFrame.from_dict(tweetdict)


# In[958]:

typeinfo


# In[959]:

retweeted = dfr['retweeted_user'].value_counts()


# In[960]:

replied = dfr['in_reply_to_screen_name'].value_counts()


# In[961]:

responsedict = {'Mean':{'Times retweeted(only including users retweeted at least once)'
                        :retweeted.mean(), 
                        'Times replied(only including users replied to at least once)'
                        :replied.mean()},
                'Standard deviation':{'Times retweeted(only including users retweeted at least once)'
                                      :retweeted.std(),
                                      'Times replied(only including users replied to at least once)'
                                      :replied.std()}}


# In[962]:

responseinfo = pd.DataFrame.from_dict(responsedict)


# In[963]:

responseinfo


# In[964]:




# In[ ]:




# In[ ]:



