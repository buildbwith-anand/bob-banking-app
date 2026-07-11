from flask import request, session, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash
from database.db import get_db


def login():
    """Handle GET (show form) and POST (validate credentials) for /login."""
    if request.method == 'GET':
        if session.get('user_id'):
            return redirect(url_for('dashboard'))
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        flash('Please enter both username and password.', 'error')
        return render_template('login.html')

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user is None or not check_password_hash(user['password'], password):
        flash('Invalid username or password.', 'error')
        return render_template('login.html')

    session.clear()
    session['user_id'] = user['id']
    session['user_name'] = user['name']
    return redirect(url_for('dashboard'))


def logout():
    """Destroy the current session and redirect to the login page."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))
