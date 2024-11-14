#importing necessary Classes
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#importing Models
from . import db
from .db_models import User,Post

#------------------------------------------------------------------------

auth = Blueprint("auth", __name__)

#USER SIGN UP
@auth.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password = request.form.get("password")

        email_exists = User.query.filter_by(email=email).first()
        user_name_exists = User.query.filter_by(user_name = user_name).first()

        if email_exists:
            flash('Email is already in use', category = 'error')
        elif user_name_exists:
            flash('This UserName is already taken', category = 'error')
        elif len(password) != 8:
            flash('Password must be of 8 characters', category ='error')
        elif len(user_name) < 2:
            flash('UserName is too short', category = 'error')
        else:
            new_user = User(email = email, user_name = user_name, password = generate_password_hash(password, method = 'pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)    
            flash("Signed in Successfully!",category = 'success')
            return redirect(url_for("views.home"))
    return render_template("signup.html")




#USER LOGIN
@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user_exists = User.query.filter_by(email = email).first()
        if user_exists:
            if check_password_hash(user_exists.password,password):
                flash('Logged in Successfully!', category = 'success')
                login_user(user_exists, remember = True)
                return redirect(url_for("views.home"))
            else:
                flash('Incorrect Password!',category = 'error') 
        else:
            flash('Incorrect Email ID', category = 'error')           

    return render_template("login.html")



#USER LOGOUT
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.start"))


#-------------------------------------------------------


#IMPLEMENTING SEARCH

#Passing search logic to the navbar
@auth.context_processor
def base():
    searched = request.form.get("searched")
    return dict(searched=searched)




#Actual Search logic
@auth.route("/search",methods=['POST'])
@login_required
def search():
    if request.method == 'POST':
        searched = request.form.get("searched")
        posts = Post.query.filter(Post.text.like('%' + searched + '%')).order_by(Post.title).all()
        return render_template("search.html",searched=searched, posts = posts)



    