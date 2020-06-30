import redis
import rq
from app import db

class Task(db.Model):
    id          = db.Column(db.String(36), primary_key=True)
    name        = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete    = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task {}>'.format(self.name)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection = current_app.redis)
        except (redis.exception.RedisError, rq.exception.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100



class User(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), index=True, unique=True)
    email         = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)