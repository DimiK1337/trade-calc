# Trade Calc — Backend 🧠📈

Backend service for **Trade Calc** — a learning-focused trading companion designed to improve  **risk management, planning discipline, and post-trade analysis** .

This API stays  **simple, explicit, and testable** : correctness first, cleverness later.

---

## Tech Stack

* **FastAPI**
* **SQLAlchemy 2.0** (ORM, typed `Mapped[]`)
* **Alembic** (migrations)
* **Pydantic v2** (schemas & validation)
* **SQLite** (dev/test) → **Postgres-ready**
* **JWT (OAuth2 password flow)** (Auth)
* **Poetry**
* **Pytest**

---

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── profile.py
│   │       │   ├── users.py          # admin-only
│   │       │   ├── trades.py         # trade journal (planned/open/closed)
│   │       │   ├── trade_images.py   # optional chart screenshot per trade
│   │       │   ├── accounts.py       # WIP
│   │       │   └── analytics.py      # WIP
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── deps.py
│   ├── crud/
│   │   ├── user.py
│   │   ├── trade.py
│   │   └── trade_image.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── init_db.py               # bootstrap root admin (optional)
│   │   └── migrations_check.py      # ensure DB is at head (startup guard)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mixins/
│   │   │   ├── timestamps.py
│   │   │   ├── trade_inputs.py
│   │   │   └── trade_outputs.py
│   │   ├── user.py
│   │   ├── trade.py
│   │   └── trade_image.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── trade.py                 # nested: inputs/outputs/journal
│   │   └── trade_image.py
│   └── main.py
├── alembic/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── utils/
│   │   └── auth.py
│   ├── test_auth.py
│   ├── test_profile.py
│   ├── test_trades.py
│   └── test_trade_images.py
├── dev.db                            # local dev DB (not committed)
├── pyproject.toml
└── README.md
```

---

## Authentication ✅

### Endpoints

| Method | Route                     | Description                       |
| -----: | ------------------------- | --------------------------------- |
|   POST | `/api/v1/auth/register` | Register new user                 |
|   POST | `/api/v1/auth/token`    | Login (email**or**username) |
|    GET | `/api/v1/auth/me`       | Get current user                  |

### Notes

* Passwords hashed with **bcrypt**
* OAuth2 password flow (`/token`) issues JWTs
* JWT **`sub` = user.id (UUID string)**

---

## Profile ✅

| Method | Route                        | Description                                            |
| -----: | ---------------------------- | ------------------------------------------------------ |
|    GET | `/api/v1/profile`          | Current user profile                                   |
|  PATCH | `/api/v1/profile`          | Update username/email (email change requires password) |
|   POST | `/api/v1/profile/password` | Change password                                        |
| DELETE | `/api/v1/profile`          | Delete account                                         |

---

## Admin ✅

* `users.is_admin` flag
* Admin-only dependency guard via `require_admin`

|            Method | Route                  | Description                          |
| ----------------: | ---------------------- | ------------------------------------ |
|               GET | `/api/v1/users`      | List all users (admin-only)          |
|               GET | `/api/v1/users/me`   | Current user (alt endpoint)          |
| PATCH/POST/DELETE | `/api/v1/users/me/*` | Self-management (UI/ops convenience) |

---

## Trades (Journal) ✅

 **Design goal** : store full “planner snapshot” (inputs + outputs) + journal fields, then query lightweight summaries.

### Endpoints

| Method | Route                   | Description                                            |
| -----: | ----------------------- | ------------------------------------------------------ |
|   POST | `/api/v1/trades`      | Create trade (planned trade journal entry)             |
|    GET | `/api/v1/trades`      | List current user’s trades (newest first)             |
|    GET | `/api/v1/trades/{id}` | Trade detail (must belong to user)                     |
|  PATCH | `/api/v1/trades/{id}` | Update limited journal fields (status/note/close info) |

### Trade schema shape (API)

* `TradeCreate` uses nested objects:
  * `inputs` (planner inputs)
  * `outputs` (planner outputs)
  * `journal` (status/note/realized values)

---

## Trade Images (Chart Screenshot) ✅

MVP: **one chart image per trade** (extensible later).

| Method | Route                         | Description                    |
| -----: | ----------------------------- | ------------------------------ |
|   POST | `/api/v1/trades/{id}/chart` | Upload chart image (multipart) |
|    GET | `/api/v1/trades/{id}/chart` | Download chart image           |
| DELETE | `/api/v1/trades/{id}/chart` | Remove chart image             |

Implementation notes:

* Stored in DB as a BLOB in a separate table (`trade_images`)
* Enforced size limits + hash checks (prevents re-uploading identical bytes)
* `GET /api/v1/trades` returns `has_charts` boolean flag for UI icon/display

---

## Database & Migrations

### Environment (.env)

```bash
DATABASE_URL=sqlite:///./dev.db
JWT_SECRET=change-me
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000

ROOT_ADMIN_EMAIL=admin@example.com
ROOT_ADMIN_USERNAME=admin
ROOT_ADMIN_PASSWORD=change-me

# Optional startup behaviors (see app/core/config.py)
BOOTSTRAP_ROOT_ADMIN=true
REQUIRE_ADMIN_ON_STARTUP=false
```

### Run migrations

```bash
poetry run alembic upgrade head
```

### Create a migration (autogenerate)

```bash
poetry run alembic revision --autogenerate -m "describe change"
```

---

## Root Admin Bootstrap (optional)

On startup, the app can create/promote a root admin using `ROOT_ADMIN_*` env vars:

* `bootstrap_root_admin()` creates the user (or promotes existing) and sets `is_admin=True`
* `ensure_admin_exists()` can fail startup if no admin exists (optional guard)

These are called in `lifespan` startup (make sure `FastAPI(..., lifespan=lifespan)` is wired).

---

## Running (Dev)

```bash
poetry install
poetry run fastapi dev app/main.py
```

* API: `http://127.0.0.1:8000`
* Docs: `http://127.0.0.1:8000/docs`

---

## Tests ✅

Covered:

* Auth (register/login/me)
* Profile (get/patch/password/delete)
* Trades (create/list/get/patch + ownership rules)
* Trade images (upload/get/delete + ownership rules)

Run all:

```bash
poetry run pytest
```

Run specific:

```bash
poetry run pytest -q tests/test_trades.py
poetry run pytest -q tests/test_trade_images.py
```

---

## Roadmap

### ✅ Done

* Auth + JWT
* Profile
* Admin bootstrap + admin-only endpoints
* Trades journal persistence (nested inputs/outputs/journal)
* Optional chart screenshot storage (DB BLOB) + summary flag
* Tests for all above

### 🚧 Next

* Frontend integration (trade planner → “Save to journal” button)
* Journal view (list + detail) + “has chart” icon
* Basic analytics (win rate, avg R, expectancy)

### ⏳ Later

* Multiple accounts
* Postgres deployment
* External object storage adapter (S3/MinIO/Vercel Blob) swap-in

---

## Philosophy

> Fewer features.
> Clear math.
> Honest feedback loops.

If it doesn’t help you trade better, it doesn’t belong here.
