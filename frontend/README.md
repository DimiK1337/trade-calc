
# 📊 Trade Calc — Frontend

Frontend for  **Trade Calc** , a personal trading tool built to enforce **risk clarity, position discipline, and deliberate trade planning** *before* execution.

Built with **Next.js (App Router)** and  **Chakra UI v3** , intentionally simple and explicit.

---

## 🎯 Purpose

Most trading mistakes don’t come from bad ideas — they come from:

* unclear risk
* oversized positions
* undefined exits
* emotional execution

This frontend exists to  **force structure before action** .

If a trade doesn’t make sense here, it shouldn’t be taken in the market.

---

## 🧠 Core Trading Concepts (Plain English)

* **LONG** → profit if price goes **up** (Buy)
* **SHORT** → profit if price goes **down** (Sell)
* **Risk** → how much money you accept losing if the stop is hit
* **1R** → that risk amount
* **rewardToRisk = 2** → potential reward is **2× risk**

No indicators. No predictions. Just math and rules.

---

## 🧮 Current Features

### ✅ Position Size Calculator (`/calculator`)

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

### 🎯 Trade Planner (`/trade-planner`)

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

## ⚠️ Important Assumptions

All calculations assume:

* ❌ No slippage
* ❌ No spread
* ❌ No commissions / fees

This is intentional.

The app shows a  **clean mathematical baseline** , not broker-specific execution noise.
Real results will always be slightly worse.

---

## 🗂 Frontend Structure

```
frontend/
├── app/
│   ├── calculator/
│   │   └── page.tsx
│   ├── trade-planner/
│   │   └── page.tsx
│   ├── components/
│   │   ├── CalculatorForm.tsx
│   │   ├── TradePlannerForm.tsx
│   │   ├── FxFields.tsx
│   │   ├── GoldFields.tsx
│   │   ├── Results.tsx
│   │   └── NavBar.tsx
│   ├── layout.tsx
│   └── page.tsx
├── lib/
│   ├── calc.ts               # position sizing logic
│   ├── tradePlanner.ts       # SL / TP math
│   ├── defaults/
│   │   ├── base.ts
│   │   ├── calculator.ts
│   │   └── tradePlanner.ts
│   └── types.ts
└── README.md
```

---

## 🧪 Design Philosophy

* All trading math lives in `/lib` (pure, deterministic, testable)
* UI must never silently “fix” invalid inputs
* Errors should stop execution, not hide risk
* Prefer clarity over cleverness
* The UI should  *slow you down* , not speed you up

---

## 🔐 Authentication (Coming Next)

The frontend will integrate with the backend to support:

* Login / Register
* JWT-based auth
* Simple user identity (initials + generated avatar color)
* Auth-gated features (saving planned trades)

No images, uploads, or profile complexity.

---

## 🔜 Planned Frontend Features

### 📓 Saved Trade Plans

* Save planned trades from Trade Planner
* Attach notes *before* execution
* View planned vs executed outcomes

### 📝 Trade Journal

* Close trades with outcome + notes
* Track R-multiple per trade
* Encourage post-trade reflection

### 📈 Analytics (Minimal, Honest)

* Win rate
* Average R
* Expectancy
* Distribution of outcomes

Tables first. Charts later.

### ⚠️ Risk Guardrails

* Max risk per trade
* Max daily loss
* Warnings when rules are violated

---

## 🚀 Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend API to be running separately.

---

## 🧘 Final Note

This app is not about prediction.
It’s about  **survival, consistency, and honesty** .

If a trade doesn’t look good  *here* ,
it won’t magically look better once money is on the line.
