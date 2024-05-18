from flask import Flask, logging
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)
    db.init_app(flaskApp)

    from app.blueprints import main
    flaskApp.register_blueprint(main)
    
    migrate = Migrate(flaskApp, db)
    login = LoginManager(flaskApp)
    login.login_view = 'login'

    if not flaskApp.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/poke_swap.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.DEBUG)
        flaskApp.logger.addHandler(file_handler)

        flaskApp.logger.setLevel(logging.DEBUG)
        flaskApp.logger.info('PokeSwap startup')
    return flaskApp

from app import routes, models