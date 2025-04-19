from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'supersekretklucz123'  # Zmień na coś bezpieczniejszego

# Ścieżki do danych watchdoga
STATUS_FILE = "/home/o11/status.json"
MPD_DIR = "/home/o11/mpd"
PARSED_DIR = "/home/o11"

# Dane logowania do panelu
USERNAME = "admin"
PASSWORD = "watchdog123"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user == USERNAME and pw == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Błędny login lub hasło")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    status = {}
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            status = json.load(f)

    mpd_files = sorted([f for f in os.listdir(MPD_DIR) if f.endswith('.mpd')])
    parsed_files = sorted([f for f in os.listdir(PARSED_DIR) if f.startswith('parsed_info')])

    return render_template('dashboard.html', status=status, mpds=mpd_files, parsed=parsed_files)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
