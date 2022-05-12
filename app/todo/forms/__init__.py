from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class add_task_form(FlaskForm):
    title = TextAreaField('Title', [validators.DataRequired()], description="Please enter the task title")
    completed = BooleanField()
    submit = SubmitField()


class edit_task_form(FlaskForm):
    submit = SubmitField()
