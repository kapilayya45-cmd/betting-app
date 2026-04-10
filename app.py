from flask import Flask, render_template, request, redirect, session
import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# DB init
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            coins INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, 1000))
            conn.commit()
        except:
            return "User already exists ❌"

        conn.close()
        return redirect('/login')

    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid login ❌"

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT coins FROM users WHERE username=?", (username,))
    coins = c.fetchone()[0]

    conn.close()

    return render_template('dashboard.html', username=username, coins=coins)

# Coin Flip Game
@app.route('/bet', methods=['GET', 'POST'])
def bet():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    if request.method == 'POST':
        amount = int(request.form['amount'])
        choice = request.form['choice']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT coins FROM users WHERE username=?", (username,))
        coins = c.fetchone()[0]

        if coins < amount:
            conn.close()
            return "Not enough coins ❌"

        flip = random.choice(["heads", "tails"])

        if choice == flip:
            coins += amount
            result = "win"
        else:
            coins -= amount
            result = "lose"

        c.execute("UPDATE users SET coins=? WHERE username=?", (coins, username))
        conn.commit()
        conn.close()

        return render_template('result.html', result=result, coins=coins, flip=flip)

    return render_template('bet.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
