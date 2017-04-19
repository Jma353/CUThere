# Imports
import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configure app
app = Flask(__name__, static_url_path='/static')
app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
db = SQLAlchemy(app)

# TODO - Load in TFIDF matrix (or compute if it's first time)

# Import + Register Blueprints
from app.events import events as events
app.register_blueprint(events)

# React Catch All Paths
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')
@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template("404.html"), 404
