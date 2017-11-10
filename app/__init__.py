"""app Package constructor"""
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config


mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(configuration):
    app = Flask(__name__)
    if not isinstance(configuration, str) and not in config.keys():
        raise TypeError('Configuration keys is not string')
    app.config.from_object(config[configuration])

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app