from flask import Flask, logging
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
moment = Moment()

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)
    
    db.init_app(flaskApp)
    migrate.init_app(flaskApp, db)
    login.init_app(flaskApp)
    moment.init_app(flaskApp)

    from app.blueprints import main as main_blueprint
    flaskApp.register_blueprint(main_blueprint)

    # Import routes after the blueprint has been registered
    from app import routes

    if not flaskApp.debug and not flaskApp.testing:
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
