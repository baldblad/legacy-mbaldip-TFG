
from flask import Flask, request, render_template, session, url_for
#import requests
import models
from flask_sqlalchemy import SQLAlchemy
#import joblib


# Declare a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/webDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    auth_id = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "Tweet({}, {}, {}, {})".format(self.id, self.auth_id, self.tag, self.created_at)


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



#@app.route('/news/histograms', methods=['GET', 'POST'])
@app.route('/news',methods=['GET', 'POST'])
def news(tab='tweets', page=1, selSDG_tweets=None):
    # Lets do some crazy stuff:
    top25 = models.getTop25()
    
    # variable declaration:
    tweet_links= []
    selAuth_hist =[]
    tweets = None
    #tab = 'hist' # default tab

    # Update database if it's needed:
    db_updated = models.updateDatabase(Tweet, db, top25)
    if db_updated:
        print('Database upfated successfully')

    # If a form is submitted
    if request.method == "POST":
        
        if 'histCheckbox' in request.form:
            selAuth_hist = request.form.get('histCheckbox')
            tab = 'hist'
        if 'tweetsCheckbox' in request.form:
            selSDG_tweets = request.form.get('tweetsCheckbox')
            tab='tweets'

    page = request.args.get('page', 1, type=int)
    selSDG_tweets = request.args.get('selSDG_tweets', None, type=int)

    #filter(Tweet.auth_id._in(selAuth_tweets))
    try:
        tweets = Tweet.query.filter_by(tag=selSDG_tweets).paginate(page=page, per_page=5)
    except:
        tweets = None

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