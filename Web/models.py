import pandas as pd

# Database management:
# initialize databases:



# return a dataframe of authority objects username:twid (key:value)
def getTop25():
    df =pd.read_csv("./database/top25.csv",
                    lineterminator='\n', index_col=0)
    return df


# return whatever, I'm gonna change my mind in 5 minutes
def tweet_links_parse(tweets):
    tweet_links=[]
    for tweet in tweets.items():
            tweet_links.append('https://twitter.com/x/status/'+str(tweet))
    return tweet_links
