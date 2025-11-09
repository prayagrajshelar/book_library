# DEVELOPMENT.md

## 🧠 Project Overview

This document explains the **development process**, **challenges**, and **solutions** followed while building the **FastAPI Book Library Management System**.

The goal of the project was to build a **fully functional REST API** for managing:
- Authors  
- Books  
- Borrow and return transactions  
with **JWT-based authentication**.

---

## 🛠️ Project Structure

book_library/
│
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response models
│   ├── database.py             # DB configuration
│   ├── auth.py                 # JWT token and password hashing logic
│   ├── routers/
│   │   ├── auth_router.py      # Register and login endpoints
│   │   ├── authors_router.py   # CRUD for authors
│   │   ├── books_router.py     # CRUD for books
│   │   └── borrow_router.py    # Borrow & return endpoints
│   └── __init__.py
│
├── .env.example                # Sample environment variables
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── DEVELOPMENT.md              # Development and debugging notes



---

## ⚙️ Development Environment Setup

- **Python Version:** 3.12  
- **Framework:** FastAPI  
- **Database:** SQLite  
- **Environment Management:** `venv`

Setup steps:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload





🚀 Testing Workflow

Register User

POST /api/v1/auth/register


Login and Copy Bearer Token

POST /api/v1/auth/login


Authorize in Swagger UI using the token.

Perform CRUD Operations:

Create Author → /api/v1/authors

Create Book → /api/v1/books

Borrow Book → /api/v1/borrow

Return Book → /api/v1/return/{record_id}

View History → /api/v1/borrow/history

📈 Future Improvements

Implement role-based permissions (Admin, User)

Add pagination and filtering for book listings

Include unit tests with pytest

Deploy using Render, Railway, or Deta

Add a frontend (React) to make it a complete full-stack app

🧩 Technologies Used
Category	Technology
Framework	FastAPI
Language	Python 3.12
ORM	SQLAlchemy
Auth	JWT (python-jose)
Hashing	passlib + bcrypt
Validation	Pydantic
Server	Uvicorn
DB	SQLite
Docs	Swagger UI (via FastAPI)



✅ Final Outcome

All CRUD endpoints tested successfully via Swagger UI

Authentication working properly (JWT tokens verified)

Database integration functioning (SQLite auto-updates)

Ready for submission and deployment