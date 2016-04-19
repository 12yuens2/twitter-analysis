import pandas as pd

def find_hashtag(row, hashtag, times):
    if hashtag in row['hashtags']:
        times.append(row['created_at'])

def get_hashtag_plot(hashtag, df):
    times = []
    df.apply(lambda row: find_hashtag (row, hashtag, times), axis=1)
    
    ones = [1] * len(times)
    idx = pd.DatetimeIndex(times)
    plot = pd.Series(ones, index=idx)
    return plot.resample('15Min').sum().fillna(0)
