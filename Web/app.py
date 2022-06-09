
from flask import Flask, request, render_template, url_for
import pandas as pd
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
    return render_template('news.html')

# Running the app
if __name__ == '__main__':
    app.run(debug = True)