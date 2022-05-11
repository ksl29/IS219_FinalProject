import logging

from flask import Blueprint, render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import TemplateNotFound
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.auth.forms import signup_form, signin_form, profile_form, security_form
from app.db import db
from app.db.models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = signup_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data),
                        fname=form.f_name.data, lname=form.l_name.data, is_admin=0)
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()

            flash('Congratulations, You are now a registered user!', "success")

            return redirect(url_for('auth.signin'), 302)

        else:
            flash('Already Registered')
            return redirect(url_for('auth.signin'), 302)
    return render_template('signup.html', form=form)


@auth.route('/signin', methods=['POST', 'GET'])
def signin():
    form = signin_form()
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.signin'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome", 'success')
            return redirect(url_for('auth.home'))
    return render_template('signin.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.signin'))


@auth.route('/home', methods=['GET'])
@login_required
def home():
    try:
        return render_template('home.html')
    except TemplateNotFound:
        abort(404)

@auth.route('/profile', methods=['GET'])
def view_profile():
    try:
        return render_template('profile_view.html')
    except TemplateNotFound:
        abort(404)
@auth.route('/profile/edit', methods=['POST', 'GET'])
def edit_profile():
    user = User.query.get(current_user.get_id())
    form = profile_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Profile', 'success')
        return redirect(url_for('auth.view_profile'))
    return render_template('profile_edit.html', form=form)


@auth.route('/account', methods=['POST', 'GET'])
def edit_account():
    user = User.query.get(current_user.get_id())
    form = security_form(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Password or Email', 'success')
        return redirect(url_for('auth.home'))
    return render_template('manage_account.html', form=form)
