from ..ext import db

# Settings Model
# This model is used for template settings
#   id as Integer - Primary Key, This is the unique ID of the user
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=False)
    app_name = db.Column(db.Text)
    dev_mode = db.Column(db.Boolean)
    