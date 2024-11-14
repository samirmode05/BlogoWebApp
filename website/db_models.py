#importing db
from . import db

#importing necessary classes
from flask_login import UserMixin
from sqlalchemy.sql import func

#----------------------------------------



#Creating Database Models


#USER MODEL
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    user_name = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(8))
    posts = db.relationship('Post', backref = 'user', lazy = 'dynamic', passive_deletes = True)
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic', passive_deletes = True)
    likes = db.relationship('Like', backref = 'user', lazy = 'dynamic', passive_deletes = True)
    followed = db.relationship('Follow',
                               foreign_keys = '[Follow.follower_id]',
                               backref = db.backref('follower',lazy = 'joined'),
                               lazy = 'dynamic',
                               cascade = 'all,delete-orphan')

    followers = db.relationship('Follow',
                               foreign_keys = '[Follow.followed_id]',
                               backref = db.backref('followed',lazy = 'joined'),
                               lazy = 'dynamic',
                               cascade = 'all,delete-orphan')

    #----------------------------------------------------------------------------------------
    
    #Creating helper methods in the User Model for all possible "follow-unfollow" operations

    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower = self, followed = user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self,user):
        f = self.followed.filter_by(followed_id = user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None




#BLOG POST MODEL
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    caption = db.Column(db.Text, nullable = True)
    text = db.Column(db.Text, nullable = False)
    image = db.Column(db.Text, nullable = False)
    filename = db.Column(db.Text, nullable = False)
    mimetype = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime(timezone = True), default = func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = 'CASCADE'), nullable = False)
    comments = db.relationship('Comment', backref = 'post', lazy = 'dynamic', passive_deletes = True)
    likes = db.relationship('Like', backref = 'post', lazy = 'dynamic', passive_deletes = True)




#FOLLOW MODEL
class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"),primary_key = True)
    followed_id = db.Column(db.Integer, db.ForeignKey("user.id"),primary_key = True)



#COMMENT MODEL
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text,nullable=False)
    timestamp = db.Column(db.DateTime(timezone = True),default = func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = 'CASCADE'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete = 'CASCADE'), nullable = False)



#LIKE MODEL
class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = 'CASCADE'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete = 'CASCADE'), nullable = False)

