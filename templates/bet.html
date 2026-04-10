@app.route('/bet', methods=['GET', 'POST'])
def bet():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount', 0))
            choice = request.form.get('choice')

            if amount <= 0:
                return "Enter valid amount ❌"

            conn = sqlite3.connect('users.db')
            c = conn.cursor()

            c.execute("SELECT coins FROM users WHERE username=?", (username,))
            data = c.fetchone()

            if not data:
                conn.close()
                return "User not found ❌"

            coins = data[0]

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

        except Exception as e:
            return f"Error: {str(e)} ❌"

    return render_template('bet.html')
