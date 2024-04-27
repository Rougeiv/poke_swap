from flask import Flask, render_template, request, redirect, session, g, jsonify
import sqlite3
import os
import random
import json

app = Flask(__name__)
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

# Routes
@app.route('/')
def index():
    signup_success = session.pop('signup_success', False)
    logged_in = session.get('logged_in', False)
    return render_template('login.html', signup_success=signup_success, logged_in=logged_in)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            # Get the database connection
            db = get_db()
            c = db.cursor()

            # Check if username already exists
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = c.fetchone()

            if existing_user:
                error_message = "Username already exists!"
                return render_template('signup.html', error_message=error_message)
            else:
                # Insert new user into the database
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                db.commit()
                # Set success message in session
                session['signup_success'] = True
                return redirect('/')
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Get the database connection
    db = get_db()
    c = db.cursor()

    # Check if username and password match
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    if user:
        # Set logged in flag in session
        session['logged_in'] = True
        session['username'] = username  # Store the username in the session
        return redirect('/game')
    else:
        error_message = "Invalid username or password!"
        return render_template('login.html', error_message=error_message)

@app.route('/main')
def main():
    return redirect('/')

@app.route('/logout')
def logout():
    # Remove user information from session
    session.pop('logged_in', None)
    return redirect('/')

# Add a new route for the game page
@app.route('/game', methods=['GET', 'POST'])
def game():

    if session.get('logged_in', False):
        if request.method == 'POST':
            try:
                username = session.get('username')
                offered_pokemon = request.json['offered_pokemon']
                desired_pokemon = request.json['desired_pokemon']

                # Get the database connection
                db = get_db('marketplace.db')
                c = db.cursor()

                # Get the current maximum trade_id
                c.execute("SELECT MAX(trade_id) FROM marketplace")
                max_trade_id = c.fetchone()[0] or 0  # Set to 0 if None

                # Insert the new trade offer into the trade_offers table
                c.execute("INSERT INTO marketplace (trade_id, user_offered, offered_pokemon, received_pokemon) VALUES (?, ?, ?, ?)",
                          (max_trade_id + 1, username, offered_pokemon, desired_pokemon))
                db.commit()

                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})

        # Render the game HTML template
        return render_template('game.html', logged_in=True)
    else:
        # Redirect to the login page if user is not logged in
        return redirect('/')

@app.route('/gacha', methods=['POST'])
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

@app.route('/gacha_one_pull', methods=['POST'])
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

@app.route('/get_trade_offers')
def get_trade_offers():
    try:
        # Connect to the marketplace database
        conn = sqlite3.connect('marketplace.db')
        c = conn.cursor()

        # Retrieve all trade offers from the database
        c.execute("SELECT * FROM marketplace")
        trade_offers = c.fetchall()

        # Close the database connection
        conn.close()

        # Convert the trade offers to a list of dictionaries for JSON response
        trade_offer_dicts = []
        for trade_offer in trade_offers:
            trade_offer_dict = {
                'trade_id': trade_offer[0],
                'user_offered': trade_offer[1],
                'offered_pokemon': trade_offer[2],
                'received_pokemon': trade_offer[3],
                'user_accepted': trade_offer[4]
            }
            trade_offer_dicts.append(trade_offer_dict)

        # Return the trade offers as JSON response
        return jsonify(trade_offer_dicts)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/post_trade', methods=['POST'])
def post_trade():
    print("post trade reached")
    try:
        username = session.get('username')
        offered_pokemon = request.json['offered_pokemon']
        desired_pokemon = request.json['desired_pokemon']

        # Get the database connection
        db = sqlite3.connect('marketplace.db')
        c = db.cursor()

        # Get the current maximum trade_id
        c.execute("SELECT MAX(trade_id) FROM marketplace")
        max_trade_id = c.fetchone()[0] or 0  # Set to 0 if None

        print("Max Trade ID:", max_trade_id)

        # Insert the new trade offer into the marketplace table
        c.execute("INSERT INTO marketplace (trade_id, user_offered, offered_pokemon, desired_pokemon) VALUES (?, ?, ?, ?)",
                  (max_trade_id + 1, username, offered_pokemon, desired_pokemon))
        db.commit()

        print("Trade offer inserted successfully.")

        return jsonify({'success': True})
    except Exception as e:
        print("Error occurred during trade insertion:", str(e))
        return jsonify({'success': False, 'error': str(e)})


@app.route('/accept_trade', methods=['POST'])
def accept_trade():
    try:
        # Get trade details from the request body
        data = request.json
        trade_id = data['trade_id']
        offered_pokemon = data['offered_pokemon']
        desired_pokemon = data['desired_pokemon']
        username = session.get('username')
        user_offered = data['user_offered']

        # Check if the user has the desired Pokemon in their inventory
        # If they do, decrement the count of that Pokemon in their inventory and update the database
        db = get_db()
        c = db.cursor()

        # Retrieve user's inventory
        c.execute("SELECT inventory FROM users WHERE username=?", (username,))
        user_inventory_json = c.fetchone()[0]
        user_inventory = json.loads(user_inventory_json)

        c.execute("SELECT inventory FROM users WHERE username=?", (user_offered,))
        offered_inventory_json = c.fetchone()[0]
        offered_inventory = json.loads(offered_inventory_json)
        print(user_offered)
        print(offered_pokemon)
        print(desired_pokemon)
        print(user_inventory)
        print(username)

        if desired_pokemon in user_inventory and user_inventory[desired_pokemon] > 0:
            # Decrement the count of desired Pokemon in the user's inventory
            user_inventory[desired_pokemon] -= 1
            print('minus the pokemon')
            user_inventory[offered_pokemon] += 1
            print('plus the pokemon')
            offered_inventory[offered_pokemon] -= 1
            print('user offered minus pokemon')
            offered_inventory[desired_pokemon] += 1
            print('user offered plus pokemon')

            # Update user's inventory in the database
            c.execute("UPDATE users SET inventory=? WHERE username=?", (json.dumps(user_inventory), username))
            c.execute("UPDATE users SET inventory=? WHERE username=?", (json.dumps(offered_inventory), user_offered))
            db.commit()
            print('updated user inventory')
            # Remove the trade offer from the marketplace
            #c.execute("DELETE FROM marketplace WHERE trade_id=?", (trade_id,))
            #db.commit()

            print('trade success')
            return jsonify({'success': True})
        else:
            # User does not have the desired Pokemon
            print('You do not have the desired Pokemon in your inventory.')
            return jsonify({'success': False, 'error': 'You do not have the desired Pokemon in your inventory.'})
    except Exception as e:
        print(str(e))
        return jsonify({'success': False, 'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
