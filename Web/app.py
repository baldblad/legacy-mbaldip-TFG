
from flask import Flask, request, render_template
import pandas as pd
import joblib


# Declare a Flask app
app = Flask(__name__)

# Main function here
@app.route('/')
def main():
    return 'This is my first ever web page UOHHOOOO!'

# Running the app
if __name__ == '__main__':
    app.run(debug = True)