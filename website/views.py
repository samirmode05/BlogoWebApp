#importing necessary classes
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

#importing models and folder path 
from .db_models import Post,User,Follow,Comment,Like
from . import db 
from .import UPLOAD_FOLDER

#importing os
import os

#importing app
from flask import current_app as app

#----------------------------------------

views = Blueprint("views",__name__)


#The starting view
@views.route("/")
def start():
    return render_template("start.html")



@views.route("/home")
@login_required
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("home.html",user = current_user, posts = posts)

#---------------------------------------------------------------------------


#View for User Profile with Basic stats
@views.route("/UserProfile/<user_name>")
@login_required
def UserProfile(user_name):
    user = User.query.filter_by(user_name = user_name).first()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("userprofile.html",user = user, posts = posts)

#---------------------------------------------------------------------------------

#Creating a Blog Post    
@views.route("/create_post", methods = ['GET','POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get("title")
        caption = request.form.get("caption")
        text = request.form.get("text")
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mimetype = image.mimetype

        if not title:
            flash('Please give a title to your post',category = 'error')
        elif not text:
            flash('Post cannot be empty', category = 'error')
        elif not image:
            flash('Please add an Image to your Post', category = 'error')     
        elif not filename:
            flash('File format not supported!',category = 'error')
        elif not mimetype:
            flash('Format not supported', category = 'error')       
        else:
            new_post = Post(title = title, caption = caption, text = text, image = image.read(), filename = filename, mimetype = mimetype, author = current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post Created', category = 'success')   
            return redirect(url_for("views.home")) 
    if request.method == 'GET':        
        return render_template("create_post.html")


#----------------------------------------------------------------------------------------------------------------------


#Blog Post Management(Delete,Edit,View)

#VIEW FOR SEARCH
@views.route("/post/<id>")
def post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("post.html",post = post)



#DELETE
@views.route("/delete/<id>")
@login_required
def delete(id):
    post = Post.query.filter_by(id = id).first()

    if current_user.id != post.author:
        flash('You can not delete others posts', category ='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted',category='success')

    return redirect(url_for("views.home"))



#EDIT
@views.route("/edit/<id>",methods = ['GET','POST'])
@login_required
def edit(id):
    post = Post.query.filter_by(id = id).first()

    if current_user.id != post.author:
        flash('You can not edit others posts', category='error')
    if request.method == 'POST':
        post.title = request.form.get("title")
        post.caption = request.form.get("caption")
        post.text = request.form.get("text")
        db.session.add(post)
        db.session.commit()
        flash("Post updated successfully",category = 'success')
    return render_template("edit_post.html")


#--------------------------------------------------------------------------------------------


# Views for Following and Unfollowing Users

#LOGIC FOR FOLLOW
@views.route('/follow/<user_name>')
@login_required
def follow(user_name):
    user = User.query.filter_by(user_name = user_name).first()
    if current_user.is_following(user):
        flash('You are already following %s.'% user_name, category = 'info')
        return redirect(url_for("views.UserProfilel", user_name = user_name))

    else:
        current_user.follow(user)
        flash('You are now following %s.'% user_name,category='success')
        return redirect(url_for("views.UserProfile", user_name=user_name))



#LOGIC FOR UNFOLLOW
@views.route('/unfollow/<user_name>')
@login_required
def unfollow(user_name):
    user = User.query.filter_by(user_name=user_name).first()
    current_user.unfollow(user)
    flash('You unfollowed %s.'% user_name,category='success')
    return redirect(url_for("views.UserProfile", user_name=user_name))





#FOLLOWERS OF AN USER & SHOWING LIST OF FOLLOWERS
@views.route('/followers/<user_name>')
def followers(user_name):
    user = User.query.filter_by(user_name = user_name).first()
    page = request.args.get('page', 1, type = int)
    pagination = user.followers.paginate(page=page,error_out=False)
    follows = [{'user': item.follower}for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           pagination=pagination,
                           follows=follows)





#NO.OF PEOPLE USER IS FOLLOWING & SHOWING THE LIST 
@views.route('/following/<user_name>')
def following(user_name):
    user = User.query.filter_by(user_name = user_name).first()
    page = request.args.get('page',1, type = int)
    pagination = user.followed.paginate(page = page,error_out = False)
    followed = [{'user': item.followed}for item in pagination.items]
    return render_template('following.html', user = user,title = "Following",
                            pagination=pagination,
                            followed = followed)

#-----------------------------------------------------------------------------------------------   
        

#CREATING & VIEWING COMMENTS
@views.route('/create_comment/<post_id>',methods = ['GET','POST'])
@login_required
def create_comment(post_id):
    if request.method == 'POST':
        text = request.form.get("text")
        if not text:
            flash("comment can not be empty",category='error')
        else:
            post = Post.query.filter_by(id = post_id)
            if post:
                comment = Comment(text = text, author = current_user.id, post_id = post_id)
                db.session.add(comment)
                db.session.commit()
                flash("You commented on this post",category = 'success')

    return render_template("create_comment.html")           


#DELETING COMMENT
@views.route('/delete_comment/<id>')
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if current_user.id != comment.author:
        flash("You cannot delete others comments",category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully",category='success')
    return redirect(url_for("views.home"))        



#-------------------------------------------------------------------------------------------------------


#LIKING POST
@views.route('/like/<post_id>')
@login_required
def like(post_id):
    post = Post.query.filter_by(id = post_id).first()
    like = Like.query.filter_by(author = current_user.id,post_id =post_id).first()
    #checking if user has already liked the post
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author = current_user.id,post_id = post_id)
        db.session.add(like)
        db.session.commit()
        flash("You liked this post",category="success")

    return redirect(url_for("views.home"))    



        