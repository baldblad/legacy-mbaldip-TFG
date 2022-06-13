
from flask import Flask, request, render_template, url_for
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
    
    # If a form is submitted
    if request.method == "POST":

        # gives the list of ids for the checked boxes with twitter account usernames
        selAuth_hist = request.form.getlist('histCheckbox')
        selAuth_tweets = request.form.getlist('tweetsCheckbox')
        
        # request filtered data in database
        tweet_links = models.getFilteredTweets(selAuth_tweets)
        
    else:
        tweet_links= []
        selAuth_tweets =[]
        selAuth_hist =[]
    return render_template('news.html', tweet_links=tweet_links,
                                        authorities=top25,
                                        selAuth_hist=selAuth_hist,
                                        selAuth_tweets=selAuth_tweets)


# Running the app
if __name__ == '__main__':
    app.run(debug = True)