"""app Package constructor"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment  # not yet had an idea of how to implement this
from flask_sqlalchemy import SQLAlchemy
from ..config import config
from .main import main as main_blueprint



bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(configuration):
    app = Flask(__name__)
    if not isinstance(configuration, str):
        raise TypeError('Configuration keys is not string')
    app.config.from_object(config[configuration])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    app.register_blueprint(main_blueprint)


    return app