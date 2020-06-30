import json
import os
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    with open(os.getcwd() + "/swagger/output/services.json") as f:
        services = json.load(f)
        return render_template('index.html', services=services)


@app.route('/services')
def services():
    with open(os.getcwd() + "/swagger/output/services.json") as f:
        services = json.load(f)
        return render_template('services.html', services=services)


@app.route('/nexus')
def nexus():
    return render_template('nexus.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/user/<username>')
#@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tasks=  [
        {'id': 'task123', 'name':'task1', 'description':'a background job', 'complete':True},
        {'id': 'task124', 'name':'task2', 'description':'still a background job', 'complete':False}
    ]
    return runder_template('user.html', user=user, tasks=tasks)