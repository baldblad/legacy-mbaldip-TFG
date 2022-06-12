
from flask import Flask, request, render_template, url_for
import requests
import models
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

@app.route('/news', methods=['GET', 'POST'])
def news():
    # Lets do some crazy stuff:
    tweet_links= []
    # If a form is submitted
    if request.method == "POST":
        
        selAuth = request.form.get('selAuth')
        # TODO: request filtered data in database
        tweets = [1535293461594767360]
        
        for tweet in tweets:
            tweet_links.append('https://twitter.com/x/status/'+str(tweet))

    return render_template('news.html',tweet_links=tweet_links)

# Running the app
if __name__ == '__main__':
    app.run(debug = True)