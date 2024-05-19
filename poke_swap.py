from flask_migrate import Migrate
from app import create_app, db
from config import DeploymentConfig
import sqlite3
import os
from flask import g
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Trade

flaskApp = create_app(DeploymentConfig)
# migrate = Migrate(db, flaskApp)
# flaskApp.secret_key = os.urandom(24)

# # Function to connect to the SQLite database
# def connect_db():
#     db = sqlite3.connect('users.db')
#     db.row_factory = sqlite3.Row
#     return db

# # Function to get the database connection
# def get_db():
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db

# # Close the database connection at the end of each request
# @flaskApp.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()

if __name__ == '__main__':
    flaskApp.run(debug=True)

@flaskApp.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Trade': Trade}