from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class add_task_form(FlaskForm):
    title = TextAreaField('Title', [validators.DataRequired()], description="Please enter the task title")
    description = TextAreaField('Description', description="Please enter a description")
    due_date = DateField('Due Date', [validators.DataRequired()])
    is_important = BooleanField('Important?')
    is_complete = BooleanField('Completed?')
    submit = SubmitField()


class edit_task_form(FlaskForm):
    title = TextAreaField('Title', [validators.DataRequired()], description="Please enter the task title")
    description = TextAreaField('Description', description="Please enter a description")
    due_date = DateField('Due Date', [validators.DataRequired()])
    is_important = BooleanField('Important?')
    is_complete = BooleanField('Completed?')
    submit = SubmitField()
