from flask import render_template
from app import app

@app.route('/')
def index():
    returnDict = {}
    returnDict['user'] = 'Dillon Friel'
    returnDict['title'] = 'Home'
    return render_template("index.html", **returnDict)