"""
Expense Tracker - Secure Flask Application
Features: Add expenses, categories, total spending summary
Security: Input validation, CSRF protection, XSS prevention, SQL injection prevention
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import sqlite3
import os
import re
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-change-in-production-12345')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# CSRF Protection
csrf = CSRFProtect(app)

# Rate Limiting (prevents brute force)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Database path
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expenses.db')

# Valid categories (whitelist)
VALID_CATEGORIES = ['food', 'transport', 'utilities', 'entertainment', 'health', 'shopping', 'education', 'other']


def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with schema"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL CHECK(amount > 0 AND amount <= 999999.99),
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', '', str(text))
    return clean[:500]


def validate_amount(amount_str):
    """Validate amount input"""
    try:
        amount = float(amount_str)
        if amount <= 0 or amount > 999999.99:
            return None
        return round(amount, 2)
    except (ValueError, TypeError):
        return None


@app.route('/')
def index():
    """Home page - show all expenses and summary"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, amount, category, description, date 
        FROM expenses 
        ORDER BY date DESC, created_at DESC
    ''')
    expenses = cursor.fetchall()
    cursor.execute('SELECT COALESCE(SUM(amount), 0) as total FROM expenses')
    total_spending = cursor.fetchone()['total']
    cursor.execute('''
        SELECT category, COALESCE(SUM(amount), 0) as total, COUNT(*) as count
        FROM expenses 
        GROUP BY category 
        ORDER BY total DESC
    ''')
    category_summary = cursor.fetchall()
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, COALESCE(SUM(amount), 0) as total
        FROM expenses 
        GROUP BY month 
        ORDER BY month DESC 
        LIMIT 6
    ''')
    monthly_summary = cursor.fetchall()
    conn.close()
    return render_template('index.html', 
                         expenses=expenses,
                         total_spending=total_spending,
                         category_summary=category_summary,
                         monthly_summary=monthly_summary,
                         categories=VALID_CATEGORIES)


@app.route('/add', methods=['POST'])
@limiter.limit("30 per minute")
def add_expense():
    """Add a new expense"""
    amount = validate_amount(request.form.get('amount'))
    if amount is None:
        flash('Invalid amount. Please enter a positive number.', 'error')
        return redirect(url_for('index'))
    category = request.form.get('category', '').lower().strip()
    if category not in VALID_CATEGORIES:
        flash('Invalid category selected.', 'error')
        return redirect(url_for('index'))
    description = sanitize_input(request.form.get('description', ''))
    date_str = request.form.get('date', '')
    try:
        expense_date = datetime.strptime(date_str, '%Y-%m-%d')
        if expense_date > datetime.now():
            flash('Date cannot be in the future.', 'error')
            return redirect(url_for('index'))
    except ValueError:
        flash('Invalid date format.', 'error')
        return redirect(url_for('index'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date_str))
    conn.commit()
    conn.close()
    flash('Expense added successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:expense_id>', methods=['POST'])
@limiter.limit("20 per minute")
def delete_expense(expense_id):
    """Delete an expense"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/api/summary')
@limiter.limit("60 per minute")
def api_summary():
    """API endpoint for summary data"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, COALESCE(SUM(amount), 0) as total
        FROM expenses 
        GROUP BY category
    ''')
    data = cursor.fetchall()
    conn.close()
    return jsonify({row['category']: row['total'] for row in data})


@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', error="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error="Something went wrong"), 500


# Initialize database on startup (works with gunicorn too)
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)