from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Load users from users.json
def load_users():
    with open('users.json') as f:
        return json.load(f)

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Check credentials
        if username in users and users[username] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try again.', 'danger')
            return render_template('login.html')

    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
