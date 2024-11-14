This is a simple social media application built using flask framework. 
Simple blogs with images can be posted by the user. The Users may as well follow each other and like and comment on each others posts.

###############################################

#Local Setup
- Clone the project

#virtual environment creation
-Go to powershell and run
    `python -m venv env`
    Activate the virtual environment by running
    `.\env\Scripts\Activate.ps1`
    Install
    `pip install flask`
    `pip install flask-sqlalchemy`
    Run
    `python .\app.py`
    -The app will run in development mode

#Folder Structure
-`website` folder contains the application code

```
|-Website
    |-auth.py (user authentication codes & search implementation)
    |-config.py (app configuration Classes)
    |-db_models.py (database Models)
    |-__init__.py (app initialization)
    |-views.py (app views codes)
    |-static (default static files folder)
        |-uploads (images uploaded by users)
    |-templates (default flask templates folder)
        |-base.html 
        |-create_comment.html 
        |-create_post.html 
        |-edit_post.html
        |-followers.html
        |-following.html
        |-home.html
        |-login.html
        |-post.html
        |-search.html
        |-signup.html
        |-start.html
        |-user_feed.html
        |-userprofile.html  
    |-__pycache__  
        |-__init__.cpython-310.pyc
        |-auth.cpython-310.pyc
        |-config.cpython-310.pyc
        |-db_models.cpython-310.pyc
        |-views.cpython-310.pyc
|-app.py (code for running the flask app)
|-README.md
|-requirements.txt (required installations)

```         