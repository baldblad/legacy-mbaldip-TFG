
from flask import Flask, request, render_template, url_for
import pandas as pd
#import joblib


# Declare a Flask app
app = Flask(__name__)


# Main function here
@app.route('/')
def index():
    return render_template('home.html')

# Running the app
if __name__ == '__main__':
    app.run(debug = True)