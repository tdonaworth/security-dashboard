import redis
import rq
from datetime import datetime
from app import db

class NexusResult(db.Model):
    row_id      = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow())
    docker_tag  = db.Column(db.String(20), default='')
    service_name= db.Column(db.String(30), default='')
    jenkins_url = db.Column(db.String(200), default='')
    nexusiq_url = db.Column(db.String(200), default='')
    yarn_log    = db.Column(db.Text, default='')

    def __repr__(self):
        return '<NexusResult id: {}, serv name: {}, cretaed: {}>'.format(self.row_id, self.service_name, self.create_date)
