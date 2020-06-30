import redis
import rq
from app import db

class Task(db.Model):
    id          = db.Column(db.String(36), primary_key=True)
    name        = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128), default='')
    complete    = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection = current_app.redis)
        except (redis.exception.RedisError, rq.exception.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100