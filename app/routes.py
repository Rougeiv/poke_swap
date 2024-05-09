from urllib.parse import urlsplit
from app import flaskApp, db
from flask import flash, logging, render_template, request, redirect, session, jsonify, url_for
import sqlite3
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
from datetime import datetime, timezone
from app.models import User, Pokemon
from app.forms import EditProfileForm, LoginForm, SignUpForm
import random
from sqlalchemy.sql.expression import func


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
    logout_user()
    return redirect(url_for('index'))

# Add a new route for the game page
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
    try:
        random_pokemon = db.session.get(Pokemon, random.randint(1, 151))
        if random_pokemon is None:
            return jsonify({'error': 'No Pokémon found'}), 404, {'Content-Type': 'application/json'}

        pokemon_data = {
        'id': random_pokemon.id,
        'pokemon_id': random_pokemon.pokedex_num,
        'name': random_pokemon.name
        }

        # now assign the pokemon to the user
        current_user.inventory.append(random_pokemon)
        db.session.commit()

        return jsonify(pokemon_data), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}
    
@flaskApp.route('/gacha_ten_pull', methods=['POST'])
def gacha_ten_pull():
    try:
        pquery = sa.select(Pokemon).order_by(func.random()).limit(10)
        random_pokemon = db.session.execute(pquery)
        if random_pokemon is None:
            return jsonify({'error': 'No Pokémon found'}), 404, {'Content-Type': 'application/json'}
        
        # Prepare a list to hold the random Pokémon data
        random_pokemon_list = []

        # Loop through each randomly selected Pokémon
        for tuple_entry in random_pokemon:
            pokemon = tuple_entry[0]
            pokemon_data = {
                'id': pokemon.id,
                'pokedex_num': pokemon.pokedex_num,
                'name': pokemon.name
            }
            random_pokemon_list.append(pokemon_data)
            
            # first check if the user already has the pokemon
            if pokemon in current_user.inventory:
                flaskApp.logger.debug('User %s already has Pokémon %s', current_user.username, pokemon.name)
            else:
                # Assign the Pokémon to the user's inventory
                current_user.inventory.append(pokemon)
                flaskApp.logger.debug('Assigned Pokémon %s to user %s', pokemon.name, current_user.username)
                flaskApp.logger.debug('Response Data: %s', jsonify({'pokemon_list': random_pokemon_list}))
        # Commit the changes to the database
        db.session.commit()

        # Return the list of randomly selected Pokémon as JSON
        return jsonify({'pokemon_list': random_pokemon_list}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        # return jsonify({'error exception': str(e)}), 500, {'Content-Type': 'application/json'}
        flaskApp.logger.error('An error occurred: %s', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

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
    form = EditProfileForm(current_user.username)
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

@flaskApp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@flaskApp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500