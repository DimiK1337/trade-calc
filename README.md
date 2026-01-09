
# 📊 Trade Calc

A personal trading tool to **plan risk, position size, and trades deliberately** — *before* clicking Buy or Sell.

Built as a  **learning system** , not a prediction engine.

---

## 🎯 Why This Exists

Most trading mistakes don’t come from bad ideas.
They come from:

* unclear risk
* oversized positions
* undefined exits
* emotional execution

**Trade Calc** exists to force clarity *before* execution and honesty *after* execution.

If a trade doesn’t look good here, it won’t magically look better in the market.

---

## 🧠 Core Trading Concepts (Plain English)

* **LONG** → profit if price goes **up**
* **SHORT** → profit if price goes **down**
* **Risk** → how much money you accept losing if the stop is hit
* **1R** → that risk amount
* **rewardToRisk = 2** → potential reward is **2× risk**

No indicators.
No predictions.
Just math and rules.

---

## 🧱 Architecture Overview

```
trade-calc/
├── frontend/   # Next.js + Chakra UI (App Router)
└── backend/    # FastAPI + SQLAlchemy + Alembic
```

Frontend and backend are intentionally **decoupled** and can evolve independently.

---

## 🖥 Frontend

**Stack**

* Next.js (App Router)
* Chakra UI v3
* TypeScript

**Purpose**

* Enforce discipline *before* a trade is taken
* Make risk explicit and hard to ignore

### Current Features

#### ✅ Position Size Calculator (`/calculator`)

**Inputs**

* Account balance
* Risk % per trade
* Stop distance (pips / ticks)
* Symbol (FX, XAUUSD)

**Outputs**

* Risk in CHF
* Lot size
* Exposure

**Question it answers**

> “How big can I trade  *without blowing up* ?”

---

#### 🎯 Trade Planner (`/trade-planner`)

**Inputs**

* Entry price
* Direction (LONG / SHORT)
* Stop distance
* Reward-to-risk (R)

**Outputs**

* Stop Loss price
* Take Profit price
* Estimated reward (CHF)

**Question it answers**

> “Is this trade worth taking *before* I place it?”

---

### Important Assumptions (Frontend)

All calculations assume:

* ❌ No slippage
* ❌ No spread
* ❌ No commissions

This is intentional.

The UI shows a  **clean mathematical baseline** , not broker execution noise.
Real trading will always be slightly worse.

---

## 🔧 Backend

**Stack**

* FastAPI
* SQLAlchemy 2.0
* Alembic
* Pydantic v2
* JWT (OAuth2 password flow)
* SQLite (dev), Postgres-ready

### Current Capabilities

#### 🔐 Authentication

* Register
* Login via **email or username**
* JWT-based auth
* `/me` endpoint
* Admin flag (`is_admin`) for protected routes

#### 🧪 Tests

* Auth flows are tested:
  * register
  * duplicate email
  * login via email
  * login via username
  * invalid credentials
  * auth-protected endpoints

Auth is intentionally  **finished and frozen** .

---

## 🧮 Design Philosophy (Shared)

* Math lives in pure functions (`/lib` on FE, services on BE)
* UI must never silently “fix” bad inputs
* Errors should stop execution, not hide risk
* Prefer clarity over cleverness
* The app should  **slow you down** , not speed you up

---

## 🔜 Roadmap (High-Level)

### Phase 1 — Trade Planning (Next)

* Authenticated users can save planned trades
* Attach notes *before* execution
* Frontend → Backend persistence

### Phase 2 — Trade Journal

* Close trades with outcome + notes
* Auto-calculate:
  * R-multiple
  * PnL
* Enforce post-trade reflection

### Phase 3 — Analytics (Minimal & Honest)

* Win rate
* Average R
* Expectancy
* Distribution of outcomes

Tables first. Charts later.

---

## 🚀 Running the Project

### Backend

```bash
cd backend
poetry install
poetry run dev
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Both services run independently.

---

## ⚠️ What This Is *Not*

Trade Calc is  **not** :

* a broker
* a signal generator
* a real-time trading platform
* an indicator playground

It is a  **decision discipline tool** .

---

## 🧘 Final Note

This app is not about prediction.
It’s about  **survival, consistency, and honesty** .

If a trade doesn’t look good  *here* ,
it won’t look better with real money on the line.
