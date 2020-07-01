import json
import os
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from app import app
from app.forms import LoginForm
from app.models import User, Task
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    with open(os.getcwd() + "/swagger/output/services.json") as f:
        services = json.load(f)
        return render_template('index.html', services=services)


@app.route('/services')
@login_required
def services():
    with open(os.getcwd() + "/swagger/output/services.json") as f:
        services = json.load(f)
        return render_template('services.html', services=services)


@app.route('/nexus')
@login_required
def nexus():
    return render_template('nexus.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tasks = [
        {'id': 'task123', 'name':'task1', 'description':'a background job', 'complete':True},
        {'id': 'task124', 'name':'task2', 'description':'still a background job', 'complete':False}
    ]
    return render_template('user.html', user=user, tasks=tasks)