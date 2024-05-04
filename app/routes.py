from urllib.parse import urlsplit
from app import flaskApp, db
from flask import flash, render_template, request, redirect, session, jsonify, url_for
import sqlite3
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
from datetime import datetime, timezone
from app.models import User
from app.forms import EditProfileForm, LoginForm, SignUpForm

@flaskApp.route('/')
@flaskApp.route('/index')
# @login_required
def index():
    # signup_success = session.pop('signup_success', False)
    # logged_in = session.get('logged_in', False)
    # , signup_success=signup_success, logged_in=logged_in
    return render_template('index.html', title='Home')

@flaskApp.route('/signup', methods=['GET', 'POST'])
def signup():
    # if request.method == 'POST':
    #     try:
    #         username = request.form['username']
    #         password = request.form['password']

    #         # Get the database connection
    #         db = get_db()
    #         c = db.cursor()

    #         # Check if username already exists
    #         c.execute("SELECT * FROM users WHERE username=?", (username,))
    #         existing_user = c.fetchone()

    #         if existing_user:
    #             error_message = "Username already exists!"
    #             return render_template('signup.html', error_message=error_message)
    #         else:
    #             # Insert new user into the database
    #             c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    #             db.commit()
    #             # Set success message in session
    #             session['signup_success'] = True
    #             return redirect('/')
    #     except Exception as e:
    #         return f"An error occurred: {str(e)}"
    # else:
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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@flaskApp.route('/main')
def main():
    return redirect(url_for('index'))

@flaskApp.route('/logout')
def logout():
    # Remove user information from session
    # session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('index'))

# Add a new route for the game page
@flaskApp.route('/catch')
def catch():
    # Check if user is logged in
    if session.get('logged_in', False):
        return render_template('catch.html', logged_in=True)
    else:
        return redirect(url_for('index'))

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
        # Connect to the Pokemon database
        conn_pokemon = sqlite3.connect('pokemon.db')
        c_pokemon = conn_pokemon.cursor()

        # Retrieve a single random Pokemon from the database
        c_pokemon.execute("SELECT id, name FROM pokemon ORDER BY RANDOM() LIMIT 1")
        pokemon = c_pokemon.fetchone()

        # Close the Pokemon database connection
        conn_pokemon.close()

        # Pass the retrieved Pokemon to the game.html template
        return jsonify(pokemon)
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

@flaskApp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')

@flaskApp.route('/how_to_play')
def how_to_play():
    return render_template('how_to_play.html')
# user profile page route
@flaskApp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or404(sa.select(User).where(User.username == username))
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
        return redirect('/user/{}'.format(current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)