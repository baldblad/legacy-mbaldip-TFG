import pandas as pd
import tweepy
import joblib
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from datetime import timedelta
#from dateutil.parser import parse
import time
# NLP
import re
#import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Database management:

# Update database if the newest item is more than a week older:
# Attributes: id, auth_id, tag, created_at
def updateDatabase(TweetDB, db, top25):
    # get newest item date of creation
    newest_date = TweetDB.query.order_by(desc(TweetDB.created_at)).first().created_at
    
    # if older than a week:
    if datetime.now()-newest_date > timedelta(days=7):
        ## connect to tweepy
        # load bearer token
        tokens = open('./database/academic research tokens.txt').readline()
        bearer_token = re.search('\w+,\s(.+)\s', tokens).group(1)
        # instantiate API endpoint and authenticate
        client = tweepy.Client(bearer_token)    

        ## get missing tweets since the newest date in the db
        df = getTimelines(client, top25['uid'], newest_date)
        print('Timelines retrieved successfully')

        ## Clean tweets and classify
        # clean
        def join_text (tweets):
            return ' '.join([w for w in tweets])

        df['clean_text']=df['text'].apply(lambda x: text_cleaner(x))
        df['clean_text']=df['clean_text'].apply(lambda x: join_text(x))
        print('Text cleaned successfully')

        # classify
        # load classifiers
        biSVM = joblib.load("./database/biSVM.pkl")
        biVectorizer = joblib.load("./database/biSVM_vectorizer.pkl")
        SDG17 = joblib.load("./database/SDG17.pkl")
        SDG17Vectorizer = joblib.load("./database/SDG17_vectorizer.pkl")
        # predict
        df['relevant_tag'] = df['clean_text'].apply(lambda x: biSVM.predict(biVectorizer.transform([x]))[0])
        df['SDGtag'] = df['clean_text'].apply(lambda x: SDG17.predict(SDG17Vectorizer.transform([x]))[0])
        print('Predictions done successfully')

        ## update database
        # keep only the tweets related to the SDGs according to the classifiers
        # also remove unnecessary attributes
        df = df[['uid','created_at','SDGtag']][df['relevant_tag']=='SDG']
        # make sure its datetime format
        df['created_at']=pd.to_datetime(df['created_at'])
        # make sure there is no duplicates
        df = df[~df.index.duplicated(keep='first')]
        # add
        # populate the database
        def populate(tweet):
            # only add if it was created exclusively after the newst stored tweet
            # and it doesn't already exist in the database

            if tweet.created_at.timestamp() > newest_date.timestamp() and db.session.query(TweetDB).get(tweet.name)==None:
                db.session.add(TweetDB(id=tweet.name, auth_id=tweet.uid, created_at=tweet.created_at, tag=tweet.SDGtag))
            return

        df.apply(lambda x: populate(x), axis=1)
        print('Items added succesfully')

        ## remove elements that are older than 30 days
        TweetDB.query.filter(datetime.now() - TweetDB.created_at > timedelta(days=30)).delete()
        print('Items removed succesfully')

        # commit to db
        db.session.commit()
        print('Session commited')

        return True
        
    return False


# text processing:
# text cleaner:
def text_cleaner(raw_text):
    # Tweet text preleaning
    def tweet_preCleaning(tweet):
        # replace endlines with spaces
        tweet = tweet.replace('\n',' ')
        
        # Remove media links and undisired characters
        return re.sub(r"(@[A-Za-z0-9_]+)|#|http\S+|sdgs?|&\w+|[^\w\s]", '', tweet)

    def stopword_removal(tweet):
        return [w for w in tweet if w not in stopwords.words('english')]

    def tweet_lemmatizing (tweet): # input: list of tokenized words from a tweet
        lemmatizer = WordNetLemmatizer() # lemmatizer instantiation
        return [lemmatizer.lemmatize(word) for word in tweet]
    
    text = tweet_preCleaning(raw_text)
    text = word_tokenize(text.lower())
    text = stopword_removal(text)
    text = tweet_lemmatizing(text)
    return text


## TWEEPY CALL
# return a dataframe containing the tweets from a set of given users and a starting datetime
def getTimelines(client, users, start_date):
    # final dataframe: (twid, uid, text, created_at) text will be substituted by tag
    timelines = dict()
    for uid in users:
    # start request
        try:
            for tweets in tweepy.Paginator(client.get_users_tweets, 
                                            uid, 
                                            exclude=['retweets','replies'],
                                            tweet_fields=['created_at','text'],
                                            max_results=100,
                                            start_time= datetime.isoformat(start_date)+'Z', #less recent
                                            end_time= datetime.now().replace(microsecond=0).isoformat()+"Z" #most recent
                                            ): 
                # wait 1 sec to avoid getting rate capped
                time.sleep(1)
                
                # store the new data in the dictionary
                if tweets.meta['result_count']>0: # if it has any referenced tweets, then store them
                    for tweet in tweets.data:
                        timelines[tweet.id] = {'uid':uid, 'text':tweet.text, 'created_at':tweet.created_at}

        # handling the exceptions
        except tweepy.errors.TweepyException as e:
            print(e)
            if e.args[0][0].code == 429: # Too many requests
                print('Two minute break. Go drink some water.')
                time.sleep(60*2)
                continue
            else:
                print('Something has gone wrong. SOS')
                break
    return pd.DataFrame.from_dict(timelines, orient='index')


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
