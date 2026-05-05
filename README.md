# Allowance Tracker

A Python-powered allowance tracker with user authentication.

## Features

- User login and sign-up
- Track allowance spending by amount, category, date, location, and description
- View a transcript of all spending entries
- Summary of total allowance, amount spent, and remaining balance
- Data saved per user in `users.json`

## Usage

1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000` in your browser and sign up or log in.

## Files

- `app.py` - Flask application with authentication
- `requirements.txt` - Python dependencies (Flask, Flask-Login)
- `templates/base.html` - Site layout
- `templates/dashboard.html` - Dashboard form and transcript
- `templates/login.html` - Login page
- `templates/signup.html` - Sign-up page
- `static/styles.css` - Styling
- `users.json` - Saved user data (generated automatically)
