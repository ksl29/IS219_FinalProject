from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class add_task_form(FlaskForm):
    title = TextAreaField('Title', [validators.DataRequired()], description="Please enter the task title")
    description = TextAreaField('Description', description="Please enter a description")
    due_date = DateTimeField('Due Date', [validators.DataRequired()], format='%Y-%m-%d')
    is_important = BooleanField('Important?', [validators.DataRequired()])
    is_completed = BooleanField('Completed?', [validators.DataRequired()])
    submit = SubmitField()


class edit_task_form(FlaskForm):
    title = TextAreaField('Title', [validators.DataRequired()], description="Please enter the task title")
    description = TextAreaField('Description', description="Please enter a description")
    due_date = DateTimeField('Due Date', [validators.DataRequired()], format='%Y-%m-%d')
    is_important = BooleanField('Important?', [validators.DataRequired()])
    is_completed = BooleanField('Completed?', [validators.DataRequired()])
    submit = SubmitField()
