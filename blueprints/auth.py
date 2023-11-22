from flask import Blueprint, redirect, render_template, url_for, session, current_app, g
from ..ext import bcrypt, login_user, db, login_required, logout_user

from ..forms.auth import LoginForm, RegisterForm, UploadForm
from ..models.user import User, Profile
from ..models.settings import Settings

# Authoriziation Blueprint
auth = Blueprint("auth",__name__)

import os

# /auth/login - Shows the login view and handles the form submission logic
@auth.route("/login",methods=("GET","POST"))
def login():
    form = LoginForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            hashpw = user.password
            if bcrypt.check_password_hash(hashpw, password):
                login_user(user)
                #Check for admin
                if user.is_admin:
                    session['admin'] = True
                session['error'] = False
                g.dev_mode = Settings.query.first().dev_mode
                return redirect(url_for("main.dashboard"))
            else:
                session['error'] = f"Invalid password for user {username}"
                return redirect(url_for("auth.login"))
        else:
            session['error'] = f"User {username} does not exist"
            return redirect(url_for("auth.login"))
    else:
        return render_template("auth/login.html",form=form)

# /auth/logout - Logs the current user out and redirects to the login page
@auth.route("/logout",methods=("GET","POST"))
@login_required
def logout():
    logout_user()
    session['admin'] = False
    session['msg'] = None
    session['error'] = None
    return redirect(url_for('auth.login'))

# /auth/register - Shows the Register view and handles the form submission logic
# NOTE: There is no logic regarding a "verification" email, the email is just more information to store about
# the user.

@auth.route("/register",methods=("GET","POST"))
def register():
    form = RegisterForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        email = form.email.data
        admin = False
        #Check if the username already exists?
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            session['error'] = f"Username {username} already taken"
            return redirect(url_for('auth.register'))
        else:
            #Check if both passwords match
            if password == password2:
                hash = bcrypt.generate_password_hash(password)
                #Check for first user - for automatic admin
                if User.query.count() == 0:
                    admin = True
                    session['admin'] = True
                
                # Generate a new Profile
                # # NOTE: We save the profile first so that we can get its ID aka new_profile.id
                # If we did not save the profile to the database the ID would be None.

                new_profile = Profile(
                    bio="New Profile",
                    status="New User"
                )
                # Add the new profile to the database
                db.session.add(new_profile)
                # Save Changes
                db.session.commit()

                # Generate a new User
                new_user = User(
                    username=username,
                    password=hash,
                    email=email,
                    is_admin=admin,
                    profile_id=new_profile.id)
                # Add the user to the database
                db.session.add(new_user)
                # Save Changes
                db.session.commit()
                
                session['error'] = False
                #Tell Flask to login the user
                login_user(new_user)
                return redirect(url_for('main.dashboard'))
            else:
                return render_template("auth/register.html",form=form,users=User.query.all())
    else:
        return render_template("auth/register.html",form=form,users=User.query.all())


@auth.route('/restore', methods=["POST"])
@login_required
def restore():
    if "admin" in session:
        if session['admin'] == True:
            print("Restoring...")
            return "OK Restore"
    else:
        return "Restore Failed: Access Denied, Not Admin"

@auth.route("/backup")
@login_required
def download_backup():
    if "admin" in session:
        if session['admin'] == True:
            print("Downloading Database Backup")
            return "OK!"
    else:
        return "Access Denied, Not Admin!"