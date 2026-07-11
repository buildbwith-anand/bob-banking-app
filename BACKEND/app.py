import os
from flask import Flask, redirect, url_for

from database.db import init_db
from controllers.auth_controller import login, logout
from controllers.account_controller import dashboard, deposit, withdraw

# Tell Flask to look for templates in the FRONTEND/ folder (one level above BACKEND/).
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '..', 'FRONTEND')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# SECRET_KEY signs the session cookie.
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod-xyz9!')


@app.route('/')
def index():
    """Root redirect -- always send to /login."""
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login_route():
    return login()


@app.route('/logout', methods=['POST'], endpoint='logout')
def logout_route():
    return logout()


@app.route('/dashboard', methods=['GET'], endpoint='dashboard')
def dashboard_route():
    return dashboard()


@app.route('/deposit', methods=['GET', 'POST'], endpoint='deposit')
def deposit_route():
    return deposit()


@app.route('/withdraw', methods=['GET', 'POST'], endpoint='withdraw')
def withdraw_route():
    return withdraw()


# Initialise the database at startup (skipped during tests via env var).
if os.environ.get('FLASK_SKIP_DB_INIT') != '1':
    with app.app_context():
        init_db()

if __name__ == '__main__':
    app.run(debug=True)
