# Banking Web Application - Implementation Plan

> **Planning level only.**

---

## 1. Solution Overview

### Objective
Build a browser-based Banking Web Application that allows customers to securely log in, view their account balance, and perform basic transactions (deposit and withdrawal).

### Functional Requirements

| # | Requirement |
|---|---|
| FR-1 | Customer can log in with valid credentials |
| FR-2 | Authenticated customer sees a dashboard |
| FR-3 | Authenticated customer can view current balance |
| FR-4 | Authenticated customer can deposit funds |
| FR-5 | Authenticated customer can withdraw funds |
| FR-6 | Customer can log out |
| FR-7 | Unauthenticated requests redirect to login |

## 2. Folder Structure

```
bob-banking-app/
|
+-- FRONTEND/          # HTML pages (Bootstrap)
+-- BACKEND/           # Python Flask application
|   +-- app.py
|   +-- controllers/
|   +-- database/
|   +-- requirements.txt
+-- tests/             # Pytest test cases
+-- .github/workflows/ # CI/CD pipeline
```
