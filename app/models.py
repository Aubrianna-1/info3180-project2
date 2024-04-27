# Add any model classes for Flask-SQLAlchemy here
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)#, autoIncrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    email = db.Column(db.String)
    location = db.Column(db.String(80))
    biography = db.Column(db.String(255))
    profilePic = db.Column(db.String(100))
    joined_on = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, firstName, lastName, email, location, biography, profilePic):
        self.username = username
        self.password = generate_password_hash(password, method="pbkdf2:sha256")
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.location = location
        self.biography = biography
        self.profilePic = profilePic
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return #unicode(self, id) #python 2 support
        except NameError:
            return str(self.id) #python 3 support
        
    def __repr__(self):
        return '<User %r>' (self.username)


class Posts(db.Model):

    id = db.Column(db.Integer, primary_key=True)#, autoIncrement=True)
    caption = db.Column(db.String)
    photo = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_on = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship("Users", backref="posts")
    
class Likes(db.Model):

    id = db.Column(db.Integer, primary_key=True)#, autoIncrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Define relationship with Users and Posts
    user = db.relationship("Users", backref="likes")
    post = db.relationship("Posts", backref="likes")

class Follows(db.Model):

    id = db.Column(db.Integer, primary_key=True)#, autoIncrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))