# bob-banking-app

Banking web application built with Flask, SQLite and Bootstrap.

## Tech Stack

| Frontend | Backend | Database |
|----------|---------|----------|
| HTML + Bootstrap | Python Flask | SQLite |

## Features

- Customer Login / Logout
- Dashboard with balance view
- Deposit Funds
- Withdraw Funds
- Session-based authentication

## Running Locally

```bash
# 1. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r BACKEND/requirements.txt

# 3. Start the app
cd BACKEND
set FLASK_APP=app.py         # Windows
# export FLASK_APP=app.py    # macOS/Linux
flask run
```

Open `http://127.0.0.1:5000` and log in with **demo / password123**.

## Running Tests

```bash
pytest tests/ -v
```
