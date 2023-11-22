from ..ext import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class SettingsForm(FlaskForm):
    app_name = StringField('App Name',validators=[DataRequired(), Length(4)])
    submit = SubmitField('Update App Name')

class BackupForm(FlaskForm):
    file = FileField('File',validators=[FileRequired(),FileAllowed(['db'], 'Databases only!')])
    submit = SubmitField('Restore Backup')