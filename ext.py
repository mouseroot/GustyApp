# Import all Flask Extensions
#   We use:
#   flask_sqlalchemy for SQL
#   flask_login for authentication
#       UserMixin - used as a base Model for handling user authentication
#       login_user - used to tell flask to login this specific user
#       logout_user - logs out the currently logged in user
#       current_user - get the currently logged in user
#       LoginManager - the actual class that handles all the login logic
#       login_required - a @dectorator to make routes require the user to be logged in to render, if not a set view is rendered instead
#           NOTE: This is perfect for stopping users from viewing pages that have logged in user data instead of checking on each route if the
#           user is logged in and handling it manaully, we can simply do
#           @main.get("/dashboard")
#           @login_required
#           def dashboard():
#               return render_template("dashboard.html")

#   flask_bcrypt for data encryption
#   flask_wtf handles forms and form submission logic

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, current_user, LoginManager, login_required
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm

from flask import current_app

# Init extension classes
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Ext functions

def config(key):
    with current_app.app_context():
        return current_app.config[key]