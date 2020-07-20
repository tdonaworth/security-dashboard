import os
import rq
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from redis import Redis
from app.debugger import initialize_flask_server_debugger_if_needed


### Used for inline VS Code debugging - see https://blog.theodo.com/2020/05/debug-flask-vscode/
initialize_flask_server_debugger_if_needed()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
#mail = Mail()
#bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.port = app.config['PORT'] or 5050
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    #mail.init_app(app)
    #bootstrap.init_app(app)
    moment.init_app(app)
    #babel.init_app(app)
    #app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('sec-dash-tasks', connection=app.redis)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.nexus import bp as nexus_bp
    app.register_blueprint(nexus_bp, url_prefix='/nexus')

    from app.services import bp as services_bp
    app.register_blueprint(services_bp, url_prefix='/services')

    ### Small work-around for sqlite issues on 'ALTER' see https://github.com/miguelgrinberg/Flask-Migrate/issues/61
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    if not app.debug:
        if app.config['SMTP_SERVER']:
            auth = None
            if app.config['SMTP_USERNAME'] or app.config['SMTP_PASSWORD']:
                auth = (app.config['SMPT_USERNAME]'], app.config['SMTP_PASSWORD'])
            secure = None
            if app.config['SMPT_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['SMTP_SERVER'], app.config['SMTP_PORT']),
                fromaddr='no-reply@' + app.config['SMTP_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Security Dashboard Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/secdash.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('SecDash startup')

    return app



from app import models
