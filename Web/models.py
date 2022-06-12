import pandas as pd


# return a dataframe of authority objects username:twid (key:value)
def getTop25():
    df =pd.read_csv("./database/top25.csv",
                    lineterminator='\n', index_col=0)
    return df


# return whatever, I'm gonna change my mind in 5 minutes
def getFilteredTweets(authIds, max_tweets=3):
    '''df =pd.read_csv("./database/top25.csv",
                    lineterminator='\n', index_col=0)
    
    for tweet in tweets:
            tweet_links.append('https://twitter.com/x/status/'+str(tweet))'''
    return
