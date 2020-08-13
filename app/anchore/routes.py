from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
#from app.anchore import AnchoreResult
from app.anchore import bp
import os, json, glob, re
import sqlite3 as sql
import sys
import requests

@bp.route('/index')
@bp.route('/<service>')
@login_required
def anchore(service=''):
    serviceFiles = glob.glob("{}/app/anchore-reports/*.json".format(os.getcwd()))
    findings = []
    services = []
    for s in serviceFiles:
        services.append(os.path.basename(s).replace('.json',''))
    
    if(service != ''):
        path = "{}/app/anchore-reports/{}.json".format(os.getcwd(), service)
        with open(path) as f:     
            findings = json.load(f)
        return render_template('anchore/index.html', services=services, findings=findings)
    else:
        return render_template('anchore/index.html', services=services)
