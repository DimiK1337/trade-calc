# Trade Calc — Backend 🧠📈

Backend service for  **Trade Calc** , a learning-focused trading companion designed to improve  **risk management, planning discipline, and post-trade analysis** .

This API is intentionally  **simple, explicit, and testable** . It prioritizes correctness and learning over premature complexity.

---

## Tech Stack

* **FastAPI** — API framework
* **SQLAlchemy 2.0** — ORM
* **Alembic** — Database migrations
* **Pydantic v2** — Schemas & validation
* **SQLite** (dev) → **Postgres-ready**
* **JWT (OAuth2 password flow)** — Authentication
* **Poetry** — Dependency & environment management
* **Pytest** — Tests

---

## Project Structure

```
Trade Calc — Backend 🧠📈backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py        # admin-only
│   │       │   ├── trades.py       # planned / executed trades (WIP)
│   │       │   └── analytics.py    # stats & metrics (WIP)
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── deps.py
│   ├── crud/
│   │   ├── user.py
│   │   ├── trade.py
│   │   └── account.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py
│   ├── models/
│   │   ├── user.py
│   │   ├── trade.py
│   │   └── account.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── trade.py
│   │   └── account.py
│   └── main.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   └── test_auth.py
├── dev.db
├── pyproject.toml
└── README.md
```

---

## Authentication (Implemented)

### Endpoints

| Method | Route                     | Description                       |
| -----: | ------------------------- | --------------------------------- |
|   POST | `/api/v1/auth/register` | Register new user                 |
|   POST | `/api/v1/auth/token`    | Login (email**or**username) |
|    GET | `/api/v1/auth/me`       | Get current user                  |

### Login rules

* Users can log in with **email or username**
* Email takes precedence if both match
* OAuth2 password flow (`/token`) is used to issue JWTs

### Security notes

* Passwords are hashed with **bcrypt**
* Password length is validated at schema level
* JWT subject currently uses user email (may switch to `user.id` later)

---

## Admin Functionality (Minimal)

* Users have an `is_admin` flag
* Admin-only routes are protected via dependency injection
* Example: list all users (no password hashes ever exposed)

---

## Database & Migrations

### Local development

* SQLite (`dev.db`)
* Alembic handles schema changes

### Run migrations

```bash
poetry run alembic upgrade head
```

### Create a migration

```bash
poetry run alembic revision --autogenerate -m "message"
```

The schema is designed to be **portable to Postgres** later without rewrites.

---

## Tests

Tests focus on  **critical behavior** , not coverage theater.

Currently covered:

* User registration
* Duplicate email handling
* Login via email
* Login via username
* Invalid credentials
* Auth-protected `/me` endpoint

Run tests:

```bash
poetry run pytest
```

---

## Running the API (Dev)

```bash
poetry install
poetry run fastapi dev app/main.py
```

Then open:

* API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## What This Backend Is *For*

This backend exists to support:

1. **Trade planning** (define risk before entering)
2. **Trade journaling** (log outcomes + mistakes)
3. **Analytics** (win rate, R-multiples, expectancy)

It is **not** meant to:

* Be a broker
* Be real-time
* Be over-engineered

---

## Roadmap (Backend)

### ✅ Done

* Auth (email / username)
* JWT + protected routes
* Migrations
* Tests

### 🚧 Next

* Save planned trades
* Close trades with outcome + notes
* Basic analytics (win rate, avg R)

### ⏳ Later

* Multiple accounts
* Postgres deployment
* Frontend-auth integration

---

## Philosophy

> Fewer features.
> Clear math.
> Honest feedback loops.

If it doesn’t help you trade better, it doesn’t belong here.
