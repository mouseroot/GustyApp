from flask import Blueprint, render_template, session, redirect, url_for, current_app, g, request
from ..ext import db, login_required, config

from ..models.user import User, Profile
from ..models.settings import Settings

from ..forms.profile import BioForm, StatusForm


# Main Blueprint
main = Blueprint("main",__name__)

# / - Index page, Clears all errors
@main.get("/")
def index():
    session['error'] = False
    
    return render_template("base.html")

@main.route("/close", methods=["GET","POST"])
def close_message():
    session['clear'] = True
    reff = request.referrer
    return redirect(reff)


# /dashboard - Show user dashboard, place to manage thier profile
@main.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    bio_form = BioForm()
    status_form = StatusForm()
    return render_template("dashboard.html",bio_form=bio_form,status_form=status_form)


# /user/<username> - View the public profile of other users
@main.get("/user/<username>")
def show_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("user.html",user=user)
    else:
        return redirect(url_for('main.index'))
