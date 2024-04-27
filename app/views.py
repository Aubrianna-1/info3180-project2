"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

<<<<<<< HEAD
import os
from app import app, db
from functools import wraps ##
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.forms import RegistrationForm, LoginForm, PostForm
from flask import render_template, request, jsonify, send_file, send_from_directory, flash, url_for, redirect, session, abort, Flask
from app.models import Users, Posts, Likes, Follows

# to handle photos for registration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
from app.models import Post,Like,Follow,User ##
from flask import render_template, request, jsonify, send_file, send_from_directory, flash, url_for, redirect, session, abort
from app.models import Users, Posts, Likes, Follows
from datetime import datetime ##
from .config import Config ##
from flask_login import login_user, logout_user, current_user, login_required ###
=======
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, send_from_directory
import os, jwt
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from app.forms import PostForm, LoginForm, RegisterForm, FollowForm
from app.models import Post, Users, Likes, Follow
from functools import wraps
from datetime import datetime, timedelta
>>>>>>> origin/login-logout

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]

    '''  #ignore this section
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'Token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401
    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated '''
#----------------------##

# USER REGISTRATION #-------------------###
@app.route('/api/v1/register', methods=['POST'])
def register():
    """Register a user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        location = form.location.data
        bio = form.bio.data
        photo_file = form.photo.data
        joined_on = datetime.utcnow()
        photo_filename = secure_filename(photo_file.filename)
        photo_file.save(os.path.join(Config.UPLOAD_FOLDER, photo_filename))

        user = User(username,password,first_name,last_name,email,location,bio,photo_filename,joined_on)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User successfully registered.",
            "username": username,
            "password": password,
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "location": location,
            "biography": bio,
            "profile_photo": photo_filename,
            "joined_on": joined_on
        }), 201
    errors = form_errors(form)
    return jsonify(errors=errors), 400
#------------------------------------##

###
# The functions below should be applicable to all Flask apps.
###
@app.route('/api/v1/register', methods=['POST'])
def register():
    form = RegistrationForm()

    # Check if the form data is valid
    if form.validate_on_submit():
        photo = form.profilePic.data 
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Extract data from the form
        username = form.username.data
        password = form.password.data
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        profilePic = filename 

        # Check if the username is already taken
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return jsonify(message="Username already exists"), 400

        # Create a new user object
        new_user = Users(username=username, password=password, firstName=firstName, 
                         lastName=lastName, email=email, location=location, 
                         biography=biography, profilePic = profilePic)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Return a success message
        return jsonify(message="User registered successfully"), 201

    # If form validation fails, return validation errors
    return jsonify(errors=form_errors(form)), 400


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


#--------------------##
# User Details
@app.route('/api/v1/users/<user_id>', methods=['GET'])
@login_required
@requires_auth
def get_user_details(user_id):
    """Returns details of the user"""
    user_details = db.session.execute(db.select(User).filter_by(id=int(user_id))).scalar()
    user_posts = db.session.execute(db.select(Post).filter_by(user_id=int(user_id))).scalars()
    user_followers = db.session.execute(db.select(Follow).filter_by(user_id=int(user_id))).scalars()
    posts = []
    followers = []
    for post in user_posts:
        posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": f"/api/v1/uploads/{post.photo}",
            "description": post.caption,
            "created_on": post.created_on,
        })
    for follower in user_followers:
        followers.append({
            "id": follower.id,
            "follower_id": follower.follower_id,
            "user_id": follower.user_id,
        })
    return jsonify({
        "id": user_details.id,
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "email": user_details.email,
        "location": user_details.location,
        "biography": user_details.biography,
        "profile_photo": f"/api/v1/uploads/{user_details.profile_photo}",
        "joined_on": user_details.joined_on.strftime("%B, %Y"),
        "posts": posts,
        "followers": followers
    }), 200
#------------------------------ POSTS ----------------------------------------------#
#View User Posts
@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@login_required
@requires_auth
def get_posts(user_id):
    """Get a list of all posts by a specific user."""
    user_posts = db.session.execute(db.select(Post).filter_by(user_id=user_id)).scalars()
    posts = []
    for post in user_posts:
        posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": f"/api/v1/posters/{post.photo}",
            "description": post.caption,
            "created_on": post.created_on,
        })
    return jsonify(posts=posts), 200

#Create User Posts  
@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@login_required
@requires_auth
def add_post(user_id):
    """Create a new post for the current logged in user."""
    postForm = NewPostForm()
    if postForm.validate_on_submit():
        photo = postForm.photo.data
        caption = postForm.caption.data
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(Config.UPLOAD_FOLDER, photo_filename))
        created_on = datetime.utcnow()
        post = Post(caption,photo_filename,user_id,created_on)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            "message": "Successfully created a new post"
        }), 201
    errors = form_errors(postForm)
    return jsonify(errors=errors), 400

#--------------##
