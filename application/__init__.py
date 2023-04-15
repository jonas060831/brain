from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_pymongo import PyMongo
import os
from flask_cors import CORS

#load the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

#setup mongodb
mongodb_client = PyMongo(app)
db = mongodb_client.db

from application import routes
