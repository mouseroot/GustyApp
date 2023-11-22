# Bootstrap Responsive Flask Template

## What is this?

This is a template for Flask and Bootstrap geared towards mobile web applications

and to help get you started with user authentification and user profiles

## Install

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf flask-bcrypt
```

Then navigate to the Root dir, the dir with `ext.py`
and run the command
```bash
bin\debug.bat
```
or naviagate to the bin directory and run `debug.bat`

## Features
- Bootstrap for style/design
- Responsive for Desktop and Mobile
- Flask for Serving the web page
    - Uses the Flask Factory pattern
    - Uses Flask Blueprints
- We utilize a few extensions to add more features
    - flask_sqlalchemy for SQL ORM
        - This project is setup for SQLite databases but mysql or mssql can be swapped within the config
    - flask_login for user authentification
    - flask_bcrypt for data encryption
    - flask_wtf for form handling logic

## Whats included?

### Models
You have 3 Models, User, Profile and Settings

#### User model
- username
- password
- email

#### Profile
- bio
- status

#### Settings
- app_name
- dev_mode

### User Authentification

Users can register a new account, login to that account and logout all out of the box.

#### Auth Blueprints

You have a single auth blueprint that handles Login, Logout and Register

#### Auth Views
The html markup renders a spiffy form for login and register that is responsive.

### User Profiles

logged in users can make changes to thier profiles
- update thier own bio
- update thier own status

### Admin Panel

A slew of features that allows you to:
 - Manage existing users and delete them
 - upload files
 - explore uploaded files
 - make changes to the website branding
 - Backup or restore the database
 - explore the database and its tables
 - put the site into developer mode / maitence mode

## Project Structure

- bin/ 
    - run.bat
    - drop.bat
    - debug.bat

- blueprints/
    - admin.py
    - auth.py
    - main.py
    - profile.py
- forms/
    - auth.py
    - profile.py
    - settings.py
- models/
    - user.py
    - settings.py
- storage/
    - static/
        - favicon.ico
        - flask-horizontal.webp
    - uploads/
- views/
    - admin/
        - browse.html
        - config.html
        - database.html
        - terminal.html
        - upload.html
        - users.html
    - auth/
        - login.html
        - register.html
    - includes/
        - navbar.html
        - messages.html
    - base.html
    - dashboard.html
    - user.html
- __init\__.py
- ext.py
- Readme.md