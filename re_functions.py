import numpy as np
import pandas as pd
import re
import json

def is_retweet(s):
    """Determines whether a tweet is a retweet"""
    
    # Match retweet in text and return True/ False if matched/not matched
    match = re.search('^RT @',s)
    if match == None:
        return False
    else: 
        return True
        
def is_reply(s):
    """Determines whether a tweet is a reply"""
    
    if pd.isnull(s):
        return False
    else: 
        return True


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


def get_hashtags(s):
    """Gets a list of hashtags in a tweet"""
    
    # match = re.findall("\"text\":\"([^\"]+)\"",s)
    # return match

    return_list = []
    json_line = json.loads(s)
    
    # Append each hashtag to list of hashtags to return
    for x in json_line['hashtags']:
        return_list.append(x['text'])
    
    return return_list


def get_mentions(s):
    """Gets a list of mentioned users in a tweet"""
    
    # match = re.findall("\"screen_name\":\"([^\"]+)\"",s)
    # return match
    return_list = []
    json_line = json.loads(s)
    
    # Append each user mentioned to list to return
    for x in json_line['user_mentions']:
        return_list.append(x['screen_name'])
                       
    return return_list

def get_retweeted(s):
    """Gets retweeted user in a retweet"""
    
    # Match user that was retweeted and return it or NaN if no match
    match = re.search("^RT @([^:]+):",s)
    if match == None:
        return np.nan
    else:
        return match.group(1)


def tweet_type(r):
    """Gets the type of tweet a row represents"""
    
    # Check for each tweet type and returns appropriate value
    if is_reply(r['in_reply_to_screen_name']):
        return "reply"
    elif is_retweet(r['text']):
        return "retweet"
    else:
        return "tweet"



def to_list(s):
    """converts a value to a list if it is not null"""
    
    # Return NaN if s is empty or s as list otherwise
    if pd.isnull(s):
        return np.nan
    else:
        return [s]