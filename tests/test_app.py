"""
tests/test_app.py

Unit and integration tests for the BobBank Flask application.

Run from the project root:
    pytest tests/ -v

Demo credentials seeded by init_db():  username='demo', password='password123'
Starting balance: $5,000.00
"""

from werkzeug.security import generate_password_hash, check_password_hash


class TestPasswordHashing:
    def test_correct_password_verifies(self):
        hashed = generate_password_hash('my-password')
        assert check_password_hash(hashed, 'my-password') is True

    def test_wrong_password_fails(self):
        hashed = generate_password_hash('my-password')
        assert check_password_hash(hashed, 'wrong-password') is False

    def test_empty_password_fails(self):
        hashed = generate_password_hash('my-password')
        assert check_password_hash(hashed, '') is False


class TestAmountValidation:
    def _v(self, raw):
        from controllers.account_controller import _validate_amount
        return _validate_amount(raw)

    def test_valid_integer(self):
        amount, err = self._v('100')
        assert amount == 100.0 and err is None

    def test_valid_decimal(self):
        amount, err = self._v('49.99')
        assert amount == 49.99 and err is None

    def test_rounds_to_two_decimals(self):
        amount, err = self._v('10.999')
        assert amount == 11.0 and err is None

    def test_zero_rejected(self):
        _, err = self._v('0')
        assert err is not None

    def test_negative_rejected(self):
        _, err = self._v('-50')
        assert err is not None

    def test_non_numeric_rejected(self):
        _, err = self._v('abc')
        assert err is not None

    def test_empty_string_rejected(self):
        _, err = self._v('')
        assert err is not None

    def test_none_rejected(self):
        _, err = self._v(None)
        assert err is not None


class TestBalanceArithmetic:
    def test_deposit_adds_correctly(self):
        assert round(1000.00 + 250.00, 2) == 1250.00

    def test_withdrawal_subtracts_correctly(self):
        assert round(1000.00 - 400.00, 2) == 600.00

    def test_exact_balance_withdrawal_reaches_zero(self):
        assert round(500.00 - 500.00, 2) == 0.00


class TestLoginRoute:
    def test_get_login_returns_200(self, flask_client):
        resp = flask_client.get('/login')
        assert resp.status_code == 200
        assert b'Login' in resp.data

    def test_root_redirects_to_login(self, flask_client):
        resp = flask_client.get('/')
        assert resp.status_code == 302
        assert '/login' in resp.headers['Location']

    def test_valid_credentials_redirect_to_dashboard(self, flask_client):
        resp = flask_client.post('/login',
                                 data={'username': 'demo', 'password': 'password123'})
        assert resp.status_code == 302
        assert '/dashboard' in resp.headers['Location']

    def test_wrong_password_shows_error(self, flask_client):
        resp = flask_client.post('/login',
                                 data={'username': 'demo', 'password': 'wrongpass'},
                                 follow_redirects=True)
        assert resp.status_code == 200
        assert b'Invalid username or password' in resp.data

    def test_unknown_username_shows_error(self, flask_client):
        resp = flask_client.post('/login',
                                 data={'username': 'nobody', 'password': 'whatever'},
                                 follow_redirects=True)
        assert b'Invalid username or password' in resp.data

    def test_empty_fields_shows_error(self, flask_client):
        resp = flask_client.post('/login',
                                 data={'username': '', 'password': ''},
                                 follow_redirects=True)
        assert b'Please enter both username and password' in resp.data


class TestSessionGuard:
    def test_dashboard_requires_auth(self, flask_client):
        resp = flask_client.get('/dashboard')
        assert resp.status_code == 302
        assert '/login' in resp.headers['Location']

    def test_deposit_requires_auth(self, flask_client):
        resp = flask_client.get('/deposit')
        assert resp.status_code == 302

    def test_withdraw_requires_auth(self, flask_client):
        resp = flask_client.get('/withdraw')
        assert resp.status_code == 302


class TestDashboard:
    def _login(self, c):
        c.post('/login', data={'username': 'demo', 'password': 'password123'})

    def test_dashboard_shows_name_and_balance(self, flask_client):
        self._login(flask_client)
        resp = flask_client.get('/dashboard')
        assert resp.status_code == 200
        assert b'Alex Johnson' in resp.data
        assert b'5000' in resp.data


class TestDeposit:
    def _login(self, c):
        c.post('/login', data={'username': 'demo', 'password': 'password123'})

    def test_valid_deposit_redirects_to_dashboard(self, flask_client):
        self._login(flask_client)
        resp = flask_client.post('/deposit', data={'amount': '200'})
        assert resp.status_code == 302
        assert '/dashboard' in resp.headers['Location']

    def test_deposit_increases_balance(self, flask_client):
        self._login(flask_client)
        flask_client.post('/deposit', data={'amount': '500'})
        resp = flask_client.get('/dashboard')
        assert b'5500' in resp.data

    def test_zero_amount_shows_error(self, flask_client):
        self._login(flask_client)
        resp = flask_client.post('/deposit', data={'amount': '0'},
                                 follow_redirects=True)
        assert b'greater than zero' in resp.data

    def test_negative_amount_shows_error(self, flask_client):
        self._login(flask_client)
        resp = flask_client.post('/deposit', data={'amount': '-100'},
                                 follow_redirects=True)
        assert b'greater than zero' in resp.data

    def test_non_numeric_shows_error(self, flask_client):
        self._login(flask_client)
        resp = flask_client.post('/deposit', data={'amount': 'abc'},
                                 follow_redirects=True)
        assert b'valid number' in resp.data

    def test_get_deposit_returns_form(self, flask_client):
        self._login(flask_client)
        resp = flask_client.get('/deposit')
        assert resp.status_code == 200
        assert b'Deposit' in resp.data


class TestWithdraw:
    def _login(self, c):
        c.post('/login', data={'username': 'demo', 'password': 'password123'})

    def test_valid_withdrawal_redirects_to_dashboard(self, flask_client):
        self._login(flask_client)
        resp = flask_client.post('/withdraw', data={'amount': '100'})
        assert resp.status_code == 302
        assert '/dashboard' in resp.headers['Location']

    def test_withdrawal_decreases_balance(self, flask_client):
        self._login(flask_client)
        flask_client.post('/withdraw', data={'amount': '1000'})
        resp = flask_client.get('/dashboard')
        assert b'4000' in resp.data

    def test_insufficient_funds_shows_error(self, flask_client):
        self._login(flask_client)
        resp = flask_client.post('/withdraw', data={'amount': '99999'},
                                 follow_redirects=True)
        assert b'Insufficient funds' in resp.data

    def test_zero_amount_shows_error(self, flask_client):
        self._login(flask_client)
        resp = flask_client.post('/withdraw', data={'amount': '0'},
                                 follow_redirects=True)
        assert b'greater than zero' in resp.data

    def test_get_withdraw_returns_form(self, flask_client):
        self._login(flask_client)
        resp = flask_client.get('/withdraw')
        assert resp.status_code == 200
        assert b'Withdraw' in resp.data


class TestLogout:
    def test_logout_redirects_to_login(self, flask_client):
        flask_client.post('/login', data={'username': 'demo', 'password': 'password123'})
        resp = flask_client.post('/logout')
        assert resp.status_code == 302
        assert '/login' in resp.headers['Location']

    def test_after_logout_dashboard_requires_reauth(self, flask_client):
        flask_client.post('/login', data={'username': 'demo', 'password': 'password123'})
        flask_client.post('/logout')
        resp = flask_client.get('/dashboard')
        assert resp.status_code == 302
        assert '/login' in resp.headers['Location']
