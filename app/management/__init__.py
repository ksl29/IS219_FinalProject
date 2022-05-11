import logging

from flask import Blueprint, render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import TemplateNotFound
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.auth.decorators import admin_required
from app.management.forms import user_edit_form, create_user_form
from app.db import db
from app.db.models import User


management = Blueprint('management', __name__, template_folder='templates')

@management.route('/users')
@login_required
@admin_required
def browse_users():
    data = User.query.all()
    titles = [('email', 'Email'), ('registered_on', 'Registered On')]
    retrieve_url = ('auth.retrieve_user', [('user_id', ':id')])
    edit_url = ('auth.edit_user', [('user_id', ':id')])
    add_url = url_for('auth.add_user')
    delete_url = ('auth.delete_user', [('user_id', ':id')])

    current_app.logger.info("Browse page loading")

    return render_template('browse.html', titles=titles, add_url=add_url, edit_url=edit_url, delete_url=delete_url,
                           retrieve_url=retrieve_url, data=data, User=User, record_type="Users")


@management.route('/users/<int:user_id>')
@login_required
def retrieve_user(user_id):
    user = User.query.get(user_id)
    return render_template('profile_view.html', user=user)


@management.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = user_edit_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        user.is_admin = int(form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash('User Edited Successfully', 'success')
        current_app.logger.info("edited a user")
        return redirect(url_for('management.browse_users'))
    return render_template('user_edit.html', form=form)


@management.route('/users/new', methods=['POST', 'GET'])
@login_required
def add_user():
    form = create_user_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data), is_admin=int(form.is_admin.data))
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you just created a user', 'success')
            return redirect(url_for('management.browse_users'))
        else:
            flash('Already Registered')
            return redirect(url_for('management.browse_users'))
    return render_template('user_new.html', form=form)


@management.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user.id == current_user.id:
        flash("You can't delete yourself!")
        return redirect(url_for('management.browse_users'), 302)
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted', 'success')
    return redirect(url_for('management.browse_users'), 302)
