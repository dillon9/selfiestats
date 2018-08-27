#twitter scraper for #mlhlocalhost in flask
#written by dillon9
#scraping logic lib written by taspinar

from flask import Flask, redirect, url_for, render_template, request
from werkzeug import secure_filename
from twitterscraper import query_tweets
app = Flask(__name__)

@app.route('/')
def index():
    x = []
    for tweet in query_tweets('#MLHLocalhost OR #mlhlocalhost OR #Mlhlocalhost'):
        x.append(tweet.text.encode('utf-8') + '<br><br>')
    return "<h1>MLH Twitter Scraper</h1><br>"+('').join(x) #This is dirty and if this was going to be expanded on, we would absolutely use templates
