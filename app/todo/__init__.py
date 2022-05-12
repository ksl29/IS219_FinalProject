from flask import Blueprint, render_template, abort, url_for, current_app, jsonify, flash
from jinja2 import TemplateNotFound
from flask_login import current_user, login_required
from sqlalchemy import desc

from app.db import db
from app.db.models import Task
from app.todo.forms import add_task_form, edit_task_form

todo = Blueprint('todo', __name__, template_folder='templates')

@todo.route('/home')
def home():
    try:
        return render_template('home.html')
    except TemplateNotFound:
        abort(404)

@todo.route('/tasks', methods=['GET'], defaults={"page": 1})
@todo.route('/tasks/<int:page>', methods=['GET'])
def browse_tasks(page):
    page = page
    per_page = 10
    pagination = Task.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    retrieve_task = ('todo.retrieve_task',[('tasks_id',':id')])
    edit_task = ('todo.edit_task',[('tasks_id',':id')])
    add_task = url_for(todo.add_task)
    delete_task = ('todo.delete_task',[('tasks_id',':id')])
    
    try:
        return render_template('browse_tasks.html', data=data,pagination=pagination, Task=Task,
                               retrieve_task=retrieve_task, edit_task=edit_task, add_task=add_task, delete_task=delete_task)
    except TemplateNotFound:
        abort(404)
 
@todo.route('/tasks/<int:tasks_id>')
@login_required       
def retrieve_task(tasks_id):
    task = Task.query.get(tasks_id)
    return render_template('view_task.html', task=task)

@todo.route('/tasks/<int:tasks_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_task():
    task = Task.query.get(tasks_id)
    form = edit_task_form(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.about.data
        task.due_date = form.due_date.data
        task.is_complete = int(form.is_admin.data)
        task.is_important = int(form.is_important.data)
        db.session.add(task)
        db.session.commit()
        flash('Task Edited Successfully', 'success')
        current_app.logger.info("edited a task")
        return redirect(url_for('todo.home'))
    return render_template('edit_task.html', form=form)

@todo.route('/tasks/new', methods=['POST', 'GET'])
@login_required
def add_task():
    form = add_task_form()
    if form.validate_on_submit():
        task = Task.query.filter_by(title=form.title.data).first()
        if task is None:
            task = Task(title=form.title.data, description=form.description.data, due_date=form.due_data.data,
                        is_important= form.is_important.data, is_complete=form.is_complete.data)
            db.session.add(task)
            db.session.commit()
            flash('Congratulations, you just created a task', 'success')
            return redirect(url_for('todo.home'))
        else:
            flash('Task already exists')
            return redirect(url_for('todo.home'))
    return render_template('add_task.html', form=form)

@todo.route('/users/<int:tasks_id>/delete', methods=['POST'])
@login_required
def delete_task():
    task = Task.query.get(tasks_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task Deleted', 'success')
    return redirect(url_for('todo.home'), 302)