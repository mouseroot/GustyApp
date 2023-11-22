from ..ext import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length

# BioForm
# This is our update bio form, we only need the bio and a submit button
class BioForm(FlaskForm):
    bio = TextAreaField('Bio')
    submit = SubmitField('Update Bio')

# StatusForm
# This is our update status form, we again only need the status and a submit button
class StatusForm(FlaskForm):
    status = TextAreaField('Status')
    submit = SubmitField('Update Status')