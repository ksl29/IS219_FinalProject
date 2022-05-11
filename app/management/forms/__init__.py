from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class create_user_form(FlaskForm):
    f_name = StringField('First Name', [
        validators.DataRequired(),

    ], description="Enter your first name")
    l_name = StringField('Last Name', [
        validators.DataRequired(),

    ], description="Enter your last name")
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ], description="You need to signup with an email")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
    is_admin = BooleanField('Admin', render_kw={'value': '1'})
    submit = SubmitField()


class user_edit_form(FlaskForm):
    about = TextAreaField('About', [validators.length(min=6, max=300)],
                          description="Please add information about yourself")
    is_admin = BooleanField('Admin', render_kw={'value': '1'})
    submit = SubmitField()
