import json
import os
from pathlib import Path
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'allowance_data.json'

app = Flask(__name__)
app.secret_key = os.getenv('ALLOWANCE_SECRET', 'dev-secret-key')


def load_data():
    if not DATA_FILE.exists():
        return {'allowance': 100.0, 'entries': []}
    with DATA_FILE.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')


@app.template_filter('currency')
def currency(value):
    return f'${value:,.2f}'


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    data = load_data()
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
                save_data(data)
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
            save_data(data)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
