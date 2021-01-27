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
from app.main import bp
import os
import json


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    with open("{}/swagger/output/services.json".format(os.getcwd())) as f:
        services = json.load(f)
        return render_template("index.html", services=services)


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


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tasks = [
        {
            "id": "task123",
            "name": "task1",
            "description": "a background job",
            "complete": True,
        },
        {
            "id": "task124",
            "name": "task2",
            "description": "still a background job",
            "complete": False,
        },
    ]
    return render_template("user.html", user=user, tasks=tasks)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
