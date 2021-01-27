from datetime import datetime
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    g,
    jsonify,
    current_app,
)
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm
from app.models import User, Task  # , Post, Message, Notification
from app.services import bp
import os
import json


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    with open("{}/swagger/output/services.json".format(os.getcwd())) as f:
        services = json.load(f)
        return render_template("services.html", services=services)


@bp.route("/services")
@login_required
def services():
    with open("{}/swagger/output/services.json".format(os.getcwd())) as f:
        services = json.load(f)
        return render_template("services.html", services=services)


@bp.route("/api/services/<service>")
def services_json(service):
    try:
        with open("{}/swagger/output/{}.json".format(os.getcwd(), service)) as f:
            service = json.load(f)
            return jsonify(service)
    except BaseException:
        return render_template("errors/404.html"), 404
