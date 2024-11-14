from flask import Blueprint

import os

config = Blueprint("config",__name__)

current_dir = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "mydatabase.sqlite3"
UPLOAD_FOLDER = os.path.join( current_dir,'static','uploads')

class Config():
    DEBUG = False
    SECRET_KEY = 'iamonline'
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = None

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(current_dir,"mydatabase.sqlite3")
    UPLOAD_FOLDER = UPLOAD_FOLDER    