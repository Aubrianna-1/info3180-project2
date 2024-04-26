"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app, db
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from werkzeug.exceptions import NotFound
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import RegistrationForm, LoginForm, PostForm
from flask import render_template, request, jsonify, send_file, send_from_directory, flash, url_for, redirect, session, abort
from app.models import Users, Posts, Likes, Follows
from flask_wtf.csrf import generate_csrf
import jwt




###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/register', methods=['POST'])
def register():
    form = RegistrationForm()

    # Check if the form data is valid
    if form.validate_on_submit():
        photo = form.photo.data 
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


#  login route      
@app.route("/api/v1/auth/login", methods=["POST"])
def login():
  """Logs a user in and returns a JWT token on successful authentication."""
  form = LoginForm()
  if not request.is_json or not form.validate_on_submit():
      return jsonify({"error": "Invalid request format or missing fields"}), 400

  username = request.json.get("username")
  password = request.json.get("password")

  if not (user := Users.query.filter_by(username=username).first()):
      return jsonify({"error": "User does not exist!"}), 401

  if not check_password_hash(user.password, password):
      return jsonify({"error": "Invalid password!"}), 401

  # Create token payload with only essential user information
  token_data = {"id": user.id}
  token = jwt.encode(token_data, app.config["SECRET_KEY"], algorithm="HS256")

  return jsonify({
      "message": "Login successful",
      "token": token
  })
    
# get a user
@app.route("/api/v1/users/<userId>", methods=["GET"])
def get_user(user_id):
  """Retrieves user information based on the provided ID or 'currentuser' keyword.
  Args:
      user_id: The user ID (integer) or 'currentuser' string.
  Returns:
      A JSON response containing user information on success or an error message.
  """

  if user_id == "currentuser":
    try:
      # Extract user ID from authorization token (improve security in production)
      user_id = extract_user_id_from_token(request.headers.get("Authorization"))
    except (KeyError, jwt.exceptions.JWTError) as e:
      return jsonify({"error": "Invalid or missing authorization token"}), 401

  user = Users.query.filter_by(id=user_id).first()

  if not user:
    raise NotFound()  # Raise a more specific exception

  # Select only necessary user fields (avoid exposing password)
  user_data = {
      "id": user.id,
      "username": user.username,
      "firstname": user.firstname,
      "lastname": user.lastname,
      "email": user.email,
      "location": user.location,
      "biography": user.biography,
      "profile_photo": "/api/v1/photo/" + user.profile,
      "joined_on": user.joined_on
  }

  return jsonify(user_data), 200

#follow a user
@app.route("/api/users/<int:user_id>/follow", methods=["POST"])
def follow(user_id):
  """Allows a user to follow another user.
  Args: user_id: The ID of the current user attempting to follow (other person).
  Returns: A JSON response indicating success or failure.
  """
  current_user = Users.query.filter_by(id=user_id).first()
  if not current_user:
    return jsonify({"error": "User does not exist"}), 404

  data = request.get_json()
  if not data or "follow_id" not in data:
    return jsonify({"error": "Missing required field: follow_id"}), 400

  other_id = data["follow_id"]
  other_user = Users.query.filter_by(id=other_id).first()
  if not other_user:
    return jsonify({"error": "other user does not exist"}), 404

  # Check if already following (optional)
  # already_following = Follows.query.filter_by(
  #     follower=current_user, currentuser=other_user
  # ).first()
  # if already_following:
  #     return jsonify({"message": "You are already following this user"}), 400

  follow = Follows(follower=current_user, currentuser=other_user)
  db.session.add(follow)
  db.session.commit()

  return jsonify({"message": f"You are now following {other_user.username}"}), 201

#adding a new post
@app.route("/api/v1/users/<userId>/posts", methods=["POST"])
def create_post(current_user_id):
    form = PostForm()
    id = current_user_id
    user = Users.query.filter_by(id=id).first()
    
    if request.method == "POST":
        if form.validate_on_submit():
           image = form.photo.data
           caption = request.form['caption']
           
           filename = secure_filename(image.filename)
           image_location = os.path.join(app.config['UPLOAD_FOLDER'],filename)
           image.save(image_location)
           newPost = Posts(photo=filename, caption=caption, user=user)
           
           db.session.add(newPost)
           db.session.commit()
           
           return jsonify({
            "message": "New Post Added"
            })
        else:
           return "Error! Something went wrong"


#to view another users posts
@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user_posts = Posts.query.filter_by(user_id=user_id).all()
        posts_list = [{'id': post.id, 'caption': post.caption, 'photo': post.photo, 'created_on': post.created_on} for post in user_posts]

        return jsonify({'user': user.username, 'posts': posts_list}), 200

    except Exception as e:
        print(e)
        jsonify(errors='An unexpecte error occurred'), 500
                        
#to like a post
@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    try:
        # Check if the post exists
        post = Posts.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        # Check if the user has already liked the post
        existing_like = Likes.query.filter_by(post_id=post_id, user_id=current_user.id).first()
        if existing_like:
            return jsonify({'message': 'You have already liked this post'}), 400

        # Create a new like for the post by the current user
        new_like = Likes(post_id=post_id, user_id=current_user.id)
        db.session.add(new_like)
        db.session.commit()

        return jsonify({'message': 'Post liked successfully'}), 200

    except Exception as e:
        print(e)
        jsonify(errors='An unexpecte error occurred'), 500
                        
#logout
@app.route("/api/v1/auth/logout", methods = ["POST"])
@login_required
def logout():
    logout_user()
    message = {'success':'Sucessfully logged out'}
    
# all posts
@app.route("/api/v1/posts", methods=["GET"])
def all_posts():
  """Retrieves and returns a list of all posts."""

  posts = Posts.query.all()
  # Use list comprehension for concise data transformation
  post_data = [
      {
          "id": post.id,
          "user_id": post.user_id,
          "photo": "/api/v1/photo/" + post.photo,
          "caption": post.caption,
          "created_at": post.created_at,
          "likes": len(post.likes)
      }
      for post in posts
  ]
  return jsonify({"posts": post_data})

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route("/api/v1/photo/<filename>", methods=['GET'])
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


###
# The functions below should be applicable to all Flask apps.
###

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