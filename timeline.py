from collections import Counter
import matplotlib.pyplot as plt
import time

# %load TwitterEval.py
#!usr/bin/env python3

def append_times(row, hashtag, times):
    if hashtag in row['hashtags']:
        times.append(row['created_at'])

def get_hashtag_plot(hashtag, df):
    times = []
    df.apply(lambda row: append_times (row, hashtag, times), axis=1)
    
    dates = times
    
    ones = [1] * len(dates)
    idx = pd.DatetimeIndex(dates)
    plot = pd.Series(ones, index=idx)
    return plot.resample('30Min').sum().fillna(0)


#total number of tweets against time
#change this later to get_hashtag_plot("digifest16")
#after cleaning hashtags with ignore case
def get_totalTweets_plot(df):
    times = []
    for time_tweeted in df.created_at:
        times.append([time_tweeted])
    dates = [t for sublist in times for t in sublist]

    ones = [1] * len(dates)
    idx = pd.DatetimeIndex(dates)
    plot = pd.Series(ones, index=idx)
    return plot.resample('30Min').sum().fillna(0)



#plot these 3 hashtags on timeline together
p1 = "learninganalytics"
p2 = "edtech"
p3 = "jisc50social"

p1_plot = get_hashtag_plot(p1, df)
p2_plot = get_hashtag_plot(p2, df)
p3_plot = get_hashtag_plot(p3, df)


df2 = pd.DataFrame({'#'+p1: p1_plot, '#'+p2: p2_plot, '#'+p3: p3_plot},
                  columns=['#'+p1, '#'+p2, '#'+p3])

df2.plot()
plt.show()