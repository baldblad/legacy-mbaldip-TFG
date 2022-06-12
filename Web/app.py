
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


@app.route('/news',methods=['GET', 'POST'])
#@app.route('/news/histograms', methods=['GET', 'POST'])
def news():
    # Lets do some crazy stuff:
    top25 = models.getTop25()
    tweet_links= []
    # If a form is submitted
    if request.method == "POST":

        # gives the list of ids for the checked boxes with twitter account usernames
        selAuth = request.form.getlist('histCheckbox')
        # TODO: request filtered data in database
        tweets = [1535293461594767360]
        
        for tweet in tweets:
            tweet_links.append('https://twitter.com/x/status/'+str(tweet))
    else:
        
        selAuth =[]
    return render_template('news.html', tweet_links=tweet_links,
                                        authorities=top25,
                                        selAuth=selAuth)


# Running the app
if __name__ == '__main__':
    app.run(debug = True)