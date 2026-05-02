# Allowance Tracker

A Python-powered allowance tracker with no login or sign-up required.

## Features

- No login or user accounts
- Track allowance spending by amount, category, date, location, and description
- View a transcript of all spending entries
- Summary of total allowance, amount spent, and remaining balance
- Data saved to `allowance_data.json`

## Usage

1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000` in your browser.

## Files

- `app.py` - Flask application
- `requirements.txt` - Python dependencies
- `templates/base.html` - Site layout
- `templates/dashboard.html` - Dashboard form and transcript
- `static/styles.css` - Styling for the Python app
- `allowance_data.json` - Saved allowance entries (generated automatically)
