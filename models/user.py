from ..ext import db, UserMixin

# User Model
# This model is our main user model, we store
#   id as Integer - Primary Key, This is the unique ID of the user
#   username as Text - the display name of the user
#   password as Text - An encrypted password
#   email as Text - users provided email
#   is_admin as Bool - A flag that determines if the user is an administrator
#   profile_id as Integer - Foriegn Key, This is the ID of the linked Profile Model

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)
    profile_id =  db.Column(db.Integer)

    # Gets the associated profile model of the user
    def profile(self):
        return Profile.query.filter_by(id=self.profile_id).first()


# Profile Model
# A linked model that holds the profile data of the corosponding user
# id as Integer - Primary Key
# bio as Text - A small bit of information about yourself that others can view
# status as Text - A small text that indicates your status to other users

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    status = db.Column(db.Text)
    