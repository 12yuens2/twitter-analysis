#!/usr/bin/env python3

import pandas as pd
import re

df = pd.read_csv('digifest2016dataset.csv')

def is_retweet(s):
    match = re.search("^RT @",s)
    if match == None:
        return False
    else: 
        return True

def is_reply(s):
    if pd.isnull(s):
        return False
    else: 
        return True

def source_name(s):
    match = re.search(">((?:\w\s?)+)</a>$",s)
    if match == None:
        return "No source found"
    else:
        return match.group(1)

def get_hashtags(s):
    match = re.findall("\"text\":\"([^\"]+)\"",s)
    return match

def get_mentions(s):
    match = re.findall("\"screen_name\":\"([^\"]+)\"",s)
    return match

df['is_retweet'] = df['text'].map(is_retweet)
df['is_reply'] = df['in_reply_to_screen_name'].map(is_reply)
df['source_name'] = df['source'].map(source_name)
df['hashtags'] = df['entities_str'].map(get_hashtags)
df['user_mentions'] = df['entities_str'].map(get_mentions)

df.to_csv('somewhat_refined.csv', index = False)
