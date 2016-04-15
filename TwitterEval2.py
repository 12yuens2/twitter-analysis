
# coding: utf-8

# In[210]:

import pandas as pd


# In[211]:

import re


# In[212]:

import matplotlib.pyplot as plt


# In[213]:

get_ipython().magic('matplotlib inline')


# In[214]:

df = pd.read_csv('digifest2016dataset.csv')


# In[215]:

df = pd.DataFrame.drop_duplicates(df)


# In[216]:

def is_retweet(s):
    match = re.search("^RT @",s)
    if match == None:
        return False
    else: 
        return True


# In[217]:

def is_reply(s):
    if pd.isnull(s):
        return False
    else: 
        return True


# In[218]:

def source_name(s):
    match = re.search(">((?:\w\s?)+)</a>$",s)
    if match == None:
        return "No source found"
    else:
        return match.group(1)


# In[219]:

def get_hashtags(s):
    match = re.findall("\"text\":\"([^\"]+)\"",s)
    return match


# In[220]:

def get_mentions(s):
    match = re.findall("\"screen_name\":\"([^\"]+)\"",s)
    return match


# In[221]:

def get_retweeted(s):
    match = re.search("^RT @([^:]+):",s)
    if match == None:
        return "No retweeted user"
    else:
        return match.group(1)


# In[222]:

def tweet_type(r):
    if is_reply(r['in_reply_to_screen_name']):
        return "reply"
    elif is_retweet(r['text']):
        return "retweet"
    else:
        return "tweet"


# In[223]:

df['is_retweet'] = df['text'].map(is_retweet)


# In[224]:

df['is_reply'] = df['in_reply_to_screen_name'].map(is_reply)


# In[225]:

df['source_name'] = df['source'].map(source_name)


# In[226]:

df['hashtags'] = df['entities_str'].map(get_hashtags)


# In[227]:

df['user_mentions'] = df['entities_str'].map(get_mentions)


# In[228]:

df['retweeted_user'] = df['text'].map(get_retweeted)


# In[229]:

df['tweet_type'] = df.apply(lambda row: tweet_type (row), axis = 1)


# In[230]:

df


# In[350]:

df.to_csv('somewhat_refined.csv', index = False)


# In[351]:

dfr = pd.read_csv('somewhat_refined.csv')


# In[352]:

sources = dfr['source_name'].value_counts()


# In[353]:

other_total = sources.select(lambda label: sources[label] < 200).sum()
sources = sources.select(lambda label: sources[label] >= 200)
sources['Other'] = other_total


# In[354]:

source_plot = sources.plot(kind="pie", title = "Applications used for posting on twitter")
source_plot.set_ylabel('')


# In[319]:

type(dfr['source_name'].value_counts())


# In[309]:

tweet_type_pie = dfr['tweet_type'].value_counts().plot(kind = 'pie', 
                                                       title = 'Distribution of types of tweets'
                                                      )
tweet_type_pie.set_ylabel('')


# In[238]:

typegroup = dfr.groupby(['tweet_type', 'from_user'])


# In[239]:

refinedtg = typegroup.size().reset_index()


# In[240]:

refinedtg.rename(columns = {0:'Number'}, inplace = True)


# In[241]:

replies = refinedtg.loc[ss3['tweet_type'] == 'reply']


# In[242]:

retweets = refinedtg.loc[ss3['tweet_type'] == 'retweet']


# In[243]:

tweets = refinedtg.loc[ss3['tweet_type'] == 'tweet']


# In[244]:

rpmean = replies.mean(0, 'Number')['Number']


# In[245]:

rtmean = retweets.mean(0, 'Number')['Number']


# In[246]:

tmean = tweets.mean(0, 'Nuumber')['Number']


# In[247]:

rpstd = replies.std(0, 'Number')['Number']


# In[248]:

rtstd = retweets.std(0, 'Number')['Number']


# In[249]:

tstd = tweets.std(0, 'Number')['Number']


# In[250]:

rpsum = replies.sum(0, 'Number')['Number']


# In[251]:

rtsum = retweets.sum(0, 'Number')['Number']


# In[252]:

tsum = tweets.sum(0, 'Number')['Number']


# In[253]:

tweetdict = {'Total':{'Tweets':tsum, 'Retweets': rtsum, 'Replies': rpsum},
            'Mean per user':{'Tweets':tmean, 'Retweets':rtmean, 'Replies':rpmean},
            'Standard deviation per user':{'Tweets':tstd, 'Retweets':rtstd, 'Replies':rpstd}}


# In[254]:

typeinfo = pd.DataFrame.from_dict(tweetdict)


# In[255]:

typeinfo


# In[ ]:




# In[ ]:



