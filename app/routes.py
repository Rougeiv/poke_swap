from urllib.parse import urlsplit
from app import flaskApp, db
from flask import flash, render_template, request, redirect, session, jsonify, url_for
import sqlite3
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
from datetime import datetime, timezone
from app.models import Pokemon, User
from app.forms import EditProfileForm, LoginForm, SignUpForm
import random

@flaskApp.route('/')
@flaskApp.route('/index')
# @login_required
def index():
    return render_template('index.html', title='Home')

@flaskApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='SignUp', form=form)

@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@flaskApp.route('/main')
def main():
    return redirect(url_for('index'))

@flaskApp.route('/logout')
def logout():
    # Remove user information from session
    logout_user()
    return redirect(url_for('index'))

# Add a new route for the game page
@login_required
@flaskApp.route('/catch')
def catch():
    # Check if user is logged in

    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('catch.html')

@flaskApp.route('/gacha', methods=['POST'])
def gacha():
    try:
        # Connect to the Pokemon database
        conn = sqlite3.connect('pokemon.db')
        c = conn.cursor()

        # Retrieve 10 random Pokemon from the database
        c.execute("SELECT id, name FROM pokemon ORDER BY RANDOM() LIMIT 10")
        pokemon = c.fetchall()

        # Close the database connection
        conn.close()

        # Return the random Pokemon data as JSON
        return jsonify(pokemon)
    except Exception as e:
        return jsonify({'error': str(e)})

@flaskApp.route('/gacha_one_pull', methods=['POST'])
def gacha_one_pull():
#     # try:
#         # # Connect to the Pokemon database
#         # conn_pokemon = sqlite3.connect('pokemon.db')
#         # c_pokemon = conn_pokemon.cursor()

#         # Retrieve a single random Pokemon from the database
#         # c_pokemon.execute("SELECT id, name FROM pokemon ORDER BY RANDOM() LIMIT 1")

#         # pokemon = c_pokemon.fetchone()

#         # Close the Pokemon database connection
#         # conn_pokemon.close()

#         # Pass the retrieved Pokemon to the game.html template
#     #     return jsonify(pokemon)
#     # except Exception as e:
#     #     return f"An error occurred: {str(e)}"
    try:
        total_pokemon_count = Pokemon.query.count()
        random_pokemon = Pokemon.query.offset(int(random.random() * total_pokemon_count)).first()

    # now assign the pokemon to the user
        current_user.inventory.append(random_pokemon)
        # return random_pokemon so it's name field can be accessed to create the path to the corresponding sprite image
        return jsonify(random_pokemon)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@flaskApp.route('/my_trades', methods=['GET'])
def my_trades():
    try:
        # Connect to the Pokemon database
        conn = sqlite3.connect('pokemon.db')
        c = conn.cursor()

        # Retrieve all trades from the database
        c.execute("SELECT * FROM trades")
        trades = c.fetchall()

        # Close the database connection
        conn.close()

        # Return the trades data as JSON
        return jsonify(trades)
    except Exception as e:
        return jsonify({'error': str(e)})
    
@flaskApp.route('/trade_offer', methods=['POST', 'GET'])
def trade_offer():
    return render_template('trade_offer.html')

@flaskApp.route('/how_to_play')
def how_to_play():
    return render_template('how_to_play.html')
# user profile page route
@flaskApp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    trades = [
        {'pokemon1': 'Pikachu', 'pokemon2': 'Charmander', 'timestamp': '2021-01-01', 'user_id1': 1, 'user_id2': 2},
        {'pokemon1': 'Bulbasaur', 'pokemon2': 'Squirtle', 'timestamp': '2021-01-02', 'user_id1': 1, 'user_id2': 2}
        ]
    return render_template('user.html', user=user, trades=trades)

@flaskApp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@flaskApp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=form.username.data))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)