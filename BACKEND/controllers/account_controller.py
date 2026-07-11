from flask import request, session, redirect, url_for, flash, render_template
from database.db import get_db


def _get_current_user():
    """Return the database row for the currently logged-in user, or None."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


def _validate_amount(raw):
    """Convert raw form string to a rounded float.

    Returns (float, None) on success or (None, error_message) on failure.
    """
    if not raw or not raw.strip():
        return None, 'Amount is required.'
    try:
        amount = float(raw)
    except ValueError:
        return None, 'Amount must be a valid number.'
    if amount <= 0:
        return None, 'Amount must be greater than zero.'
    return round(amount, 2), None


def dashboard():
    """GET /dashboard -- display account summary for the logged-in user."""
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user = _get_current_user()
    if user is None:
        session.clear()
        return redirect(url_for('login'))

    return render_template('dashboard.html',
                           user_name=user['name'],
                           balance=user['balance'])


def deposit():
    """GET /deposit -- show form.  POST /deposit -- add funds to balance."""
    if not session.get('user_id'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('deposit.html')

    amount, error = _validate_amount(request.form.get('amount'))
    if error:
        flash(error, 'error')
        return render_template('deposit.html')

    conn = get_db()
    conn.execute(
        "UPDATE users SET balance = balance + ? WHERE id = ?",
        (amount, session['user_id'])
    )
    conn.commit()
    conn.close()

    flash(f'Successfully deposited ${amount:,.2f} to your account.', 'success')
    return redirect(url_for('dashboard'))


def withdraw():
    """GET /withdraw -- show form.  POST /withdraw -- deduct funds from balance."""
    if not session.get('user_id'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('withdraw.html')

    raw_amount = request.form.get('amount')

    # Validation check 1: amount field must not be empty
    if not raw_amount or not raw_amount.strip():
        flash('Amount is required', 'error')
        return render_template('withdraw.html')

    # Validation check 2: amount must be a positive number
    try:
        amount_value = float(raw_amount)
    except ValueError:
        amount_value = 0
    if amount_value <= 0:
        flash('Amount must be greater than zero', 'error')
        return render_template('withdraw.html')

    # Validation check 3: amount must not exceed current balance
    user = _get_current_user()
    if amount_value > user['balance']:
        flash('Insufficient funds', 'error')
        return render_template('withdraw.html')

    amount, error = _validate_amount(raw_amount)
    if error:
        flash(error, 'error')
        return render_template('withdraw.html')

    conn = get_db()
    conn.execute(
        "UPDATE users SET balance = balance - ? WHERE id = ?",
        (amount, session['user_id'])
    )
    conn.commit()
    conn.close()

    flash(f'Successfully withdrew ${amount:,.2f} from your account.', 'success')
    return redirect(url_for('dashboard'))
