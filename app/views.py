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
from app.forms import RegistrationForm, LoginForm, PostForm
from flask import render_template, request, jsonify, send_file, send_from_directory, flash, url_for, redirect, session, abort, Flask
from app.models import Users, Posts, Likes, Follows

# to handle photos for registration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


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