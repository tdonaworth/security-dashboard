from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.nexus.nexusresult import NexusResult#, Post, Message, Notification
from app.nexus import bp
import os, json
import sqlite3 as sql

@bp.route('/')
@bp.route('/index')
#@login_required
def nexus():
    return render_template('nexus/index.html')

@bp.route('/addrec', methods=['GET', 'POST'])
def addrec():
    if request.method == 'POST':
        try:
            create_date  = request.form['create_date']
            docker_tag   = request.form['docker_tag']
            service_name = request.form['service_name']
            jenkins_url  = request.form['jenkins_url']
            nexusiq_url  = request.form['nexusiq_url']
            yarn_log     = request.form['yarn_log']
            
            rec = NexusResult(create_date=create_date, \
                                docker_tag=docker_tag, \
                                service_name=service_name, \
                                jenkins_url=jenkins_url, \
                                nexusiq_url=nexusiq_url, \
                                yarn_log=yarn_log)
            db.session.add(rec)
            db.session.commit()
            msg = "Record successfully added"

            return render_template("nexus/index.html", msg=msg)
        except:
            db.session.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("nexus/index.html",msg = msg)

@bp.route('/list', methods = ['GET'])
def list():
    all_results = NexusResult.query.all()
    return render_template("nexus/list.html",rows = all_results)

@bp.route('/addLatestRec',methods = ['POST'])
def addLatestRec():
    if request.method == 'POST':
        try:
            docker_tag   = request.form['docker_tag']
            service_name = request.form['service_name']
            jenkins_url  = request.form['jenkins_url']
            nexusiq_url  = request.form['nexusiq_url']
            yarn_log     = request.form['yarn_log']
            
            with sql.connect("latestDatabase.db") as con:
                try:
                    cur = con.cursor()
                    
                    cur.execute("REPLACE INTO NEXUS_LATEST_RESULTS (docker_tag,service_name,jenkins_url,nexusiq_url,yarn_log) \
                        VALUES (?,?,?,?,?)",(docker_tag,service_name,jenkins_url,nexusiq_url,yarn_log) )
                    
                    con.commit()
                    msg = "Record successfully added"
                    print(msg)
                except:
                    con.rollback()
                    msg = "error in insert operation"
                finally:
                    con.close()
        except:
            msg = "error in insert operation"
        finally:
            return render_template("nexus/results.html",msg = msg)

@bp.route('/listLatest',methods = ['GET'])
def listLatest():
   con = sql.connect("latestDatabase.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from NEXUS_LATEST_RESULTS where docker_tag in ('latest', 'master') order by docker_tag ASC, service_name ASC")
   
   rows = cur.fetchall();
   con.close()
   return render_template("nexus/listLatest.html",rows = rows)
   
   
'''
@bp.route('/addLatestRec', methods = ['POST'])
def addLatestRec():
    if request.method == 'POST':
        try:
            docker_tag   = request.form['docker_tag']
            service_name = request.form['service_name']
            jenkins_url  = request.form['jenkins_url']
            nexusiq_url  = request.form['nexusiq_url']
            yarn_log     = request.form['yarn_log']
            #cur.execute("REPLACE INTO NEXUS_LATEST_RESULTS (docker_tag,service_name,jenkins_url,nexusiq_url,yarn_log) VALUES (?,?,?,?,?)",(docker_tag,service_name,jenkins_url,nexusiq_url,yarn_log) )
            
            rec = NexusResult(docker_tag=docker_tag, \
                    service_name=service_name, \
                    jenkins_url=jenkins_url, \
                    nexusiq_url=nexusiq_url, \
                    yarn_log=yarn_log)
            db.session.update(rec)
            db.session.commit()
            msg = "Record successfully added"
            return render_template("nexus/index.html", msg=msg)
        except:
            db.session.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("nexus/index.html",msg = msg)
'''