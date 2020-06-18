import json
import os
from flask import render_template
from app import app

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