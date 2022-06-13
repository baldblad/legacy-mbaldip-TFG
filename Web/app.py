
from flask import Flask, request, render_template, session, url_for
import requests
import models
from flask_sqlalchemy import SQLAlchemy
#import joblib


# Declare a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/webDB.db'
db = SQLAlchemy(app)

class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    auth_id = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "Tweet({}, {}, {})".format(self.id, self.auth_id, self.tag)


'''# initialize database
@app.before_first_request()
def initialize_databases():
    return
'''
# Main function here
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/wordclouds')
def wordclouds():
    return render_template('wordclouds.html')


@app.route('/news',methods=['GET', 'POST'])
#@app.route('/news/histograms', methods=['GET', 'POST'])
def news():
    # Lets do some crazy stuff:
    top25 = models.getTop25()
    
    # variable declaration:
    tweet_links= []
    selSDG_tweets =[]
    selAuth_hist =[]
    tweets = []
    tab = 'hist' # default tab

    # If a form is submitted
    if request.method == "POST":
        
        if 'histCheckbox' in request.form:
            selAuth_hist = request.form.getlist('histCheckbox')
            tab = 'hist'
        if 'tweetsCheckbox' in request.form:
            selSDG_tweets = request.form.getlist('tweetsCheckbox')
            tab='tweets'
            print(selSDG_tweets[0])
            # request filtered data in database
            page = request.args.get('page', 1, type=int)
            #filter(Tweet.auth_id._in(selAuth_tweets))
            tweets = Tweet.query.filter_by(tag=selSDG_tweets[0]).paginate(page=page, per_page=3)

            print(tweets)
            #tweet_links=["https://twitter.com/x/status/807811447862468608",
                       # "https://twitter.com/x/status/807811447862468608" ]
            #tweet_links = models.tweet_links_parse(tweets) # not used Nor tested

    return render_template('news.html', tweet_links=tweet_links,
                                        authorities=top25,
                                        SDGs=[i for i in range(1,18)],
                                        selAuth_hist=selAuth_hist,
                                        selAuth_tweets=selSDG_tweets,
                                        tweets=tweets,
                                        tab=tab)


# Running the app
if __name__ == '__main__':
    app.run(debug = True)