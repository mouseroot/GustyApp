# Bootstrap Responsive Flask Template

## What is this?

This is a template to get you started with Flask and Bootstrap geared towards mobile web applications

This is to help get you started with user authentification and user profiles


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
You have 2 Models, User and Profile

#### User model
- username
- password
- email

#### Profile
- bio
- status

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

Very basic admin panel to view or delete the registered users

## Project Structure

- bin/ 
    - run.bat
    - debug.bat
- blueprints/
    - admin.py
    - auth.py
    - main.py
    - profile.py
- forms
    - auth.py
    - profile.py
- models
    - user.py
- storage
    - static/
    - uploads/
- views
    - admin/
    - auth/
    - includes/
    - base.html
    - dashboard.html
    - user.html
- __init\__.py
- ext.py
- Readme.md