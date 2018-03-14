"""app Package constructor"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(configuration):
    app = Flask(__name__)
    if configuration not in config.keys():
        raise TypeError('Unexpected Configuration key')
    app.config.from_object(config[configuration])

    db.init_app(app)
    from .main import main 
    app.register_blueprint(main)
    return app