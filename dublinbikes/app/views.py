from flask import render_template
from app import app

@app.route('/')
def index():
    returnDict = {}
    returnDict['user'] = 'User123'
    returnDict['title'] = 'Dublin Bikes'
    return render_template("index.html", **returnDict)