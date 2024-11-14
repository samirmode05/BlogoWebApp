#Importing necessary Classes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Importing OS
import os
from os import path

#Importing config to configure app
from .config import config
from .config import LocalDevelopmentConfig


#-------------------------------------------

#Specifying path
current_dir = os.path.abspath(os.path.dirname(__file__))

#defining db
db = SQLAlchemy()

#The File for Database and Folder for Uploading Images
DB_NAME = "mydatabase.sqlite3"
UPLOAD_FOLDER = os.path.join('static','uploads')


#Creating App
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    #registering Blueprints with app
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    
    
    #Importing Dtabase Models
    from .db_models import User,Post,Follow,Comment,Like

    #Creating the database
    with app.app_context():
        db.create_all()

    #Configuring and Initialising LoginManagerand it's view
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    #user_loader callback to reload the user object from user ID stored in the session
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

        
    return app






