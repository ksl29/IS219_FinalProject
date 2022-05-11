from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class signup_form(FlaskForm):
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
    submit = SubmitField()


class signin_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=8, max=35)
    ])
    submit = SubmitField()