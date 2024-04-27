from app import app
from flask import Flask, render_template, request, redirect, session, g, jsonify

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

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
@app.route('/game')
def game():
    # Check if user is logged in
    if session.get('logged_in', False):
        return render_template('game.html', logged_in=True)
    else:
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
