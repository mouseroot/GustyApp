from flask import Blueprint, redirect, render_template, url_for, session, current_app, g
from ..ext import bcrypt, login_user, db, login_required, logout_user, current_user

# Grab Both Login and Register forms
from ..forms.auth import LoginForm, RegisterForm, UploadForm

# Grab Settings 
from ..forms.settings import SettingsForm, BackupForm

# Grab the User model
from ..models.user import User, Profile
from ..models.settings import Settings

# Grab the Setting model
from ..models.settings import Settings

# Get secure_filename function from core-lib
from werkzeug.utils import secure_filename

import os

# Create the admin blueprint
admin = Blueprint("admin",__name__)


@admin.route("/browse")
@login_required
def browse():
    uploads = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template("admin/browse.html",files=uploads)

@admin.route("/terminal")
@login_required
def terminal():
    return render_template("admin/terminal.html")

# /admin/users - Manage all the users
@admin.route("/users",methods=("GET","POST"))
@login_required
def users():
    if current_user.is_admin:
        all_users = User.query.all()
        return render_template("admin/users.html",users=all_users,form=UploadForm())
    else:
        return redirect(url_for("main.index"))
    
# /admin/remove/<id> - Remove selected user
@admin.post("/remove/<id>")
@login_required
def remove(id):
    print(f"Removing {id}")
    user = User.query.filter_by(id=int(id))
    if user:
        pid = user.first().profile().id
        _profile = Profile.query.filter_by(id=pid)
        _profile.delete()
        user.delete()
    db.session.commit()
    return redirect(url_for('admin.users'))

# /setup - Install page
@admin.route("/config",methods=["GET","POST"])
@login_required
def config():
    if "admin" in session and session['admin'] == True:
        settings_form = SettingsForm()
        backup_form = BackupForm()
        init_config = Settings.query.filter_by(id=1).first()
        if session.get("admin") == False:
            return redirect(url_for("main.index"))
        if settings_form.is_submitted():
            init_config.app_name = settings_form.app_name.data
            init_config.dev_mode = False
            print(f"\tSaving Data: {settings_form.app_name.data}")
            db.session.commit()
            g.app_name = settings_form.app_name.data
            return redirect(url_for('main.index'))
        else:
            return render_template("admin/config.html",form=settings_form,backup_form=backup_form)
    else:
        return redirect(url_for("main.index"))

@admin.route("/developer")
@login_required
def switch_mode():
    if "admin" in session:
        if session['admin'] == True:
            g.dev_mode = not g.dev_mode
            Settings.query.filter_by(id=1).first().dev_mode = g.dev_mode
            db.session.commit()
    return redirect(url_for('main.index'))

@admin.route("/database")
@login_required
def explore_database():
    if "admin" in session:
        if session['admin'] == True:
            return render_template("admin/database.html",profiles=Profile.query.all(),users=User.query.all(),setting=Settings.query.first())
    else:
        return redirect(url_for('main.index'))

@admin.route("/upload", methods=["GET","POST"])
@login_required
def upload():
    if "admin" in session and session['admin'] == True:
        upload_form = UploadForm()
        if upload_form.is_submitted():
            form_data = upload_form.file.data
            if form_data:
                upload_filename = secure_filename(form_data.filename)
                upload_ext = upload_filename.split(".")[-1]
                dir = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_filename)
                #Check if really an image
                form_data.save(dir)
                session['message'] = f"File {upload_filename} was uploaded!"
                return redirect(url_for('admin.users'))
        else:
            return render_template("admin/upload.html",form=upload_form)
    else:
        return redirect(url_for("main.index"))