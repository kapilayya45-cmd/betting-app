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

        result = random.choice(["heads", "tails"])

        if choice == result:
            coins += amount
            outcome = "win"
        else:
            coins -= amount
            outcome = "lose"

        c.execute("UPDATE users SET coins=? WHERE username=?", (coins, username))
        conn.commit()
        conn.close()

        return render_template('result.html', result=outcome, coins=coins, flip=result)

    return render_template('bet.html')
