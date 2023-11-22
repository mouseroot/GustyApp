from ..ext import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

# LoginForm
# This is our login form we only need the username and the password of the user and a submit button
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Login')

# RegisterForm
# This is a registration form, we require 2 passwords to make sure they match and an email just for fun

# NOTE: We use the Length Validator to tell the form that it must be ATLEAST 4 chars
# This works on the browser side to prevent the form from being submitted if these conditions are not met.
class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(4)])
    password = PasswordField('Password',validators=[DataRequired(), Length(4)])
    password2 = PasswordField('Password Again',validators=[DataRequired(), Length(4)])
    email = EmailField('Email',validators=[DataRequired()])
    submit = SubmitField('Create Account')


# Upload Form
class UploadForm(FlaskForm):
    file = FileField('File',validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload File')