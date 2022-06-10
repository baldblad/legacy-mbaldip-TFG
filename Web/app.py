
from flask import Flask, request, render_template, url_for
import pandas as pd
import requests
#import joblib


# Declare a Flask app
app = Flask(__name__)


# Main function here
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/wordclouds')
def wordclouds():
    return render_template('wordclouds.html')

@app.route('/news')
def news():
    # Lets do some crazy stuff:
    tweets = [1534897204934189058]
    tweet_links= []
    for tweet in tweets:
        tweet_links.append('https://twitter.com/x/status/'+str(tweet))

    return render_template('news.html',tweet_links=tweet_links)

# Running the app
if __name__ == '__main__':
    app.run(debug = True)