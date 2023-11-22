#
#   Entrypoint
#      
#   NOTE: This template uses the "Factory" pattern( https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/ )
#   
#
#   This is the main entrypoint of our application, either flask will load this file
#   via commandline like: flask --app folder_name run
#   and look for the create_app function and attempt to call it,
#   OR another WSGI Wrapper will load this file and serve the application.

from flask import Flask, render_template, redirect, url_for, session, g, request
from .ext import login_manager, bcrypt, db

# Import Blueprints
from .blueprints.main import main
from .blueprints.auth import auth
from .blueprints.admin import admin
from .blueprints.profile import profile

# Import Models
from .models.user import User, Profile
from .models.settings import Settings

# Import Forms
from .forms.settings import SettingsForm

# Import built-in modules
import os

# Get the Absolute path to this file.
basedir = os.path.abspath(os.path.dirname(__file__))


#   Create App Factory Function
#   This is our actual entrypoint
#
def create_app():
    # Flask App
    app = Flask(
        __name__,
        template_folder="views",
        static_folder="storage/static"
    )

    # Config SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'storage/database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Config Secret Key used in generating unique form tokens during submission.
    app.config['SECRET_KEY'] = str(os.urandom(28)) + "@#$%^sddsth92nszflyjdkl45lspass__code__"

    # Debug Config
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Upload Config
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'storage/static/uploads/')

    # Login Config
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Extensions
    #  
    # NOTE: These are imported and inialized in ext.py
    # All we have todo is call the appropriate init method passing in our app

    # Init the Database
    db.init_app(app)

    # Init the Login Manager
    login_manager.init_app(app)

    # Configure the login manager to redirect to this view if we use @login_required and the user is NOT logged in.
    login_manager.login_view = "auth.login"

    # Init the BCrypt Module
    bcrypt.init_app(app)

    # Template Filters
    #
    # NOTE: These are made avaliable in all templates we use
    # We use them by specifing the function name we specified after a |
    # For example we could say in the template markup
    #
    #   {{ current_user.id | get_username}}
    #
    #   This would pass in current_user.id to the 
    #   function get_username_by_id and render what is returned.
    @app.template_filter('get_username')
    def get_username_by_id(id):
        user = User.query.filter_by(id=int(id)).first()
        if user:
            return user.username
    
    # Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth,url_prefix="/auth")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(profile, url_prefix="/profile")
    
    with app.app_context() as ctx:
        # Build tables from models
        db.create_all()
        
        if Settings.query.count() == 0:
            print("\tSettings Initialized")
            boot_settings = Settings(app_name="Flask Template",dev_mode=True)
            db.session.add(boot_settings)
            db.session.commit()

        g.dev_mode = True
        
    """
        @app.before_request
        def load_settings():
            g.app_name = Settings.query.filter_by(id=1).first().app_name
            if request.method == "GET":
                if Settings.query.filter_by(id=1).first().dev_mode == True:
                    settings_form = SettingsForm()
                    return render_template("setup.html",form=settings_form)
                else:
                    return None
            else:
                return None


    """
    # Before the request happens
    @app.before_request
    def load_settings():
        g.app_name = Settings.query.filter_by(id=1).first().app_name
        g.dev_mode = Settings.query.filter_by(id=1).first().dev_mode
        # Clear Messages from the session
        if 'clear' in session:
            if session['clear'] == True:
                session['message'] = False
                session['error'] = False
                session['clear'] = False

        


    return app
