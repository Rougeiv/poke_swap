from app import app
import sqlite3
import os
from flask import g
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Trade

app.secret_key = os.urandom(24)

# Function to connect to the SQLite database
def connect_db():
    db = sqlite3.connect('users.db')
    db.row_factory = sqlite3.Row
    return db

# Function to get the database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Close the database connection at the end of each request
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Trade': Trade}