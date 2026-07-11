# Banking Web Application - Step-by-Step Implementation Guide

> **Plain-English Instructions Only.**

---

## 1. Environment Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
3. Install dependencies: `pip install flask werkzeug pytest`
4. Freeze requirements: `pip freeze > BACKEND/requirements.txt`

## 2. Backend

- `BACKEND/database/db.py` - SQLite connection, table creation, seed demo account
- `BACKEND/controllers/auth_controller.py` - login/logout logic
- `BACKEND/controllers/account_controller.py` - dashboard, deposit, withdraw
- `BACKEND/app.py` - Flask app, route registration

## 3. Frontend

- `FRONTEND/login.html` - login form
- `FRONTEND/dashboard.html` - balance display and action buttons
- `FRONTEND/deposit.html` - deposit form
- `FRONTEND/withdraw.html` - withdrawal form

## 4. Testing

Run `pytest tests/ -v` from the project root.
