from flask import Flask
from flask_login import LoginManager ##
from .config import Config
<<<<<<< HEAD
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
=======
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
>>>>>>> origin/login-logout

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

<<<<<<< HEAD
db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here
migrate = Migrate(app, db)

from app import views
=======
csfr = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
>>>>>>> origin/login-logout
