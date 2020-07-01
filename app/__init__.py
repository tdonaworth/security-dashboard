from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from redis import Redis
import rq
#from debugger import initialize_flask_server_debugger_if_needed

#initialize_flask_server_debugger_if_needed()

app = Flask(__name__)
app.config.from_object(Config)
app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue('sec-dash-tasks', connection = app.redis)

login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

### Small work-around for sqlite issues on 'ALTER' see https://github.com/miguelgrinberg/Flask-Migrate/issues/61
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


from app import routes, models