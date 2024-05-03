from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/how_to_play')
def how_to_play():
    return render_template('howtoplay.html')

@app.route('/catch')
def catch():
    return render_template('catch.html')

@app.route('/trade_request')
def trade_request():
    return render_template('traderequest.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/trade_offer')
def trade_offer():
    return render_template('tradeoffer.html')

if __name__ == '__main__':
    app.run(debug=True)
