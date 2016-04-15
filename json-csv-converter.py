#!/usr/bin/env python3

import sys
import json
import pandas as pd
from datetime import datetime
import numpy as np

def get_nullable(line, field):

    #nullables to NaN if null, for same format as TAG
    val = np.nan
    if line[field] is not None:
            val = line[field]
            return val

def make_status_url(line):
    return ('http://twitter.com/' 
           + line['user']['screen_name'] 
           + '/statuses/' 
           + line['id_str']
           )

def get_coord(line):
    coord = np.nan
    if line['coordinates'] is not None:
        coord = ("loc: " 
                + str(line['coordinates']['coordinates'][0]) 
                + ',' 
                + str(line['coordinates']['coordinates'][1])
                )
        return coord

def get_time(line):
    dt_time = datetime.strptime(line['created_at'],'%a %b %d %H:%M:%S %z %Y' )
    return dt_time.strftime('%d/%m/%Y %H:%M:%S')

def generate_table(file_name, result_name):
    json_file = open(file_name, 'r')
    invalid_tweets = 0
    df = pd.DataFrame(columns = ['id_str', 
                                 'from_user', 
                                 'text', 
                                 'created_at', 
                                 'time', 
                                 'geo_coordinates', 
                                 'user_lang', 
                                 'in_reply_to_user_id_str', 
                                 'in_reply_to_screen_name', 
                                 'from_user_id_str', 
                                 'in_reply_to_status_id_str', 
                                 'source', 
                                 'profile_image_url', 
                                 'user_followers_count', 
                                 'user_friends_count',
                                 'status_url',
                                 'entities_str'
                                ])

    for index, line in enumerate(json_file):
        json_line = json.loads(line)
            
        # Check id_str in line to avoid lines representing deleted tweets
        if 'id_str' in json_line:
                        
            df.loc[index - invalid_tweets] = [json_line['id_str'], 
                                              json_line['user']['screen_name'], 
                                              json_line['text'], 
                                              json_line['created_at'], 
                                              get_time(json_line), 
                                              get_coord(json_line), 
                                              get_nullable(json_line, 'lang'), 
                                              get_nullable(json_line, 'in_reply_to_user_id_str'), 
                                              get_nullable(json_line, 'in_reply_to_screen_name'), 
                                              json_line['user']['id_str'], 
                                              get_nullable(json_line, 'in_reply_to_status_id_str'), 
                                              json_line['source'], 
                                              json_line['user']['profile_image_url'], 
                                              json_line['user']['followers_count'], 
                                              json_line['user']['friends_count'],
                                              make_status_url(json_line),
                                              json_line['entities']
                                             ]
        else:
            invalid_tweets = invalid_tweets + 1

    df.to_csv(result_name + '.csv', index = False)


if __name__ == "__main__":
    if len(sys.argv) != 3: # check number of arguments
        print("usage ./json-csv-converter.py <json twitter filename> <name of results file to create>")
        sys.exit(0) # exit with return value of 0
    
    try:
        generate_table(sys.argv[1], sys.argv[2])
    except FileNotFoundError:
        print('Specified file not found')
    except:
        print("Error: ", sys.exc_info()[0])
