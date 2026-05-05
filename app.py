import json
import os
from pathlib import Path
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / 'users.json'

app = Flask(__name__)
app.secret_key = os.getenv('ALLOWANCE_SECRET', 'dev-secret-key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, password_hash=None, data=None):
        self.id = username
        self.password_hash = password_hash
        self.data = data or {'allowance': 100.0, 'entries': []}

def load_users():
    if not USERS_FILE.exists():
        return {}
    with USERS_FILE.open('r', encoding='utf-8') as handle:
        return json.load(handle)

def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2), encoding='utf-8')

@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    if user_id in users:
        return User(user_id, users[user_id]['password_hash'], users[user_id]['data'])
    return None

@app.template_filter('currency')
def currency(value):
    return f'${value:,.2f}'


@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    data = current_user.data
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_allowance':
            allowance_value = request.form.get('allowance')
            try:
                amount = float(allowance_value)
            except (TypeError, ValueError):
                amount = 0.0

            if amount <= 0:
                flash('Allowance must be a positive number.', 'danger')
            else:
                data['allowance'] = amount
                users = load_users()
                users[current_user.id]['data'] = data
                save_users(users)
                flash('Allowance amount updated.', 'success')
            return redirect(url_for('dashboard'))

        if action == 'save_entry':
            amount_value = request.form.get('amount')
            category = request.form.get('category', '').strip()
            location = request.form.get('location', '').strip()
            entry_date = request.form.get('date', '').strip()
            description = request.form.get('description', '').strip()

            try:
                amount = float(amount_value)
            except (TypeError, ValueError):
                amount = 0.0

            if amount <= 0 or not category or not location or not entry_date:
                flash('Enter a valid amount, category, location, and date.', 'danger')
                return redirect(url_for('dashboard'))

            data['entries'].append({
                'amount': amount,
                'category': category,
                'location': location,
                'date': entry_date,
                'description': description,
            })
            users = load_users()
            users[current_user.id]['data'] = data
            save_users(users)
            flash('Allowance entry saved.', 'success')
            return redirect(url_for('dashboard'))

    spent = sum(entry.get('amount', 0) for entry in data.get('entries', []))
    remaining = data.get('allowance', 0) - spent
    return render_template(
        'dashboard.html',
        data=data,
        spent=spent,
        remaining=remaining,
        today=date.today().isoformat(),
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        
        users = load_users()
        if username in users and check_password_hash(users[username]['password_hash'], password):
            user = User(username, users[username]['password_hash'], users[username]['data'])
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            users = load_users()
            if username in users:
                flash('Username already exists.', 'danger')
            else:
                password_hash = generate_password_hash(password)
                users[username] = {'password_hash': password_hash, 'data': {'allowance': 100.0, 'entries': []}}
                save_users(users)
                user = User(username, password_hash, users[username]['data'])
                login_user(user)
                flash('Account created successfully.', 'success')
                return redirect(url_for('dashboard'))
    
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
