# 📊 Trade Calc App

A personal trading tool to **plan risk, position size, and trades deliberately** — before clicking Buy or Sell.

Built with **Next.js (App Router)** + **Chakra UI v3**, designed to stay simple, explicit, and hard to misuse.

---

## 🧠 Core Ideas

Trading mistakes usually come from:
- unclear risk
- oversized positions
- undefined exits

This app exists to **force clarity before execution**.

---

## 🚦 Core Concepts (Plain English)

- **LONG** → profit if price goes **up** (Buy)
- **SHORT** → profit if price goes **down** (Sell)

- **Risk** = how much money you are willing to lose if the stop is hit  
- **1R** = that risk amount  
- **rewardToRisk = 2** → target profit is **2× the risk**

---

## 🧮 Current Features

### ✅ Position Size Calculator (`/calculator`)
- Inputs:
  - Account balance
  - Risk % per trade
  - Stop distance (pips / ticks)
  - Symbol (FX, XAUUSD)
- Outputs:
  - Risk in CHF
  - Lot size
  - Exposure
- Purpose:
  - “How big can I trade *without blowing up*?”

---

### 🎯 Trade Planner (`/trade-planner`)
- Inputs:
  - Entry price
  - Direction (Buy / Sell)
  - Stop distance
  - Reward-to-risk (R)
- Outputs:
  - Stop Loss price
  - Take Profit price
  - Estimated reward in CHF
- Purpose:
  - “Is this trade worth taking *before* I place it?”

---

## ⚠️ Important Assumptions (Read This)

The calculations assume:
- ❌ **No slippage** (stops execute exactly at price)
- ❌ **No spread**
- ❌ **No commissions / fees**

👉 Real trading will be *slightly worse* than the calculator.  
This is intentional: the math shows the **best-case baseline**, not broker reality.

---

## 🗂 Project Structure

```
frontend/
├── app/
│ ├── calculator/
│ ├── trade-planner/
│ └── layout.tsx
├── components/
│ ├── CalculatorForm.tsx
│ ├── TradePlannerForm.tsx
│ ├── FxFields.tsx
│ ├── GoldFields.tsx
│ ├── Results.tsx
│ └── NavBar.tsx
├── lib/
│ ├── calc.ts # position sizing logic
│ ├── tradePlanner.ts # SL / TP computation
│ ├── defaults/
│ │ ├── base.ts
│ │ ├── calculator.ts
│ │ └── tradePlanner.ts
│ └── types.ts
```

---

## 🧪 Design Philosophy

- Math lives in `/lib` (pure, testable)
- UI should never silently “fix” bad inputs
- Errors should stop execution, not hide risk
- Prefer clarity over cleverness

---

## 🔜 Next Steps (Planned)

### 📓 Trade Journal
- Store each planned & executed trade
- Track:
  - R-multiple per trade
  - win rate
  - drawdowns
- View performance over time, not just single trades

### 📈 Analytics
- Equity curve (CHF + R)
- Average R per trade
- Best / worst sessions
- Risk-adjusted performance

### 👤 Accounts
- Multiple accounts (demo, live, prop)
- Separate risk rules per account
- Switch accounts from UI

### ⚠️ Risk Guardrails
- Max risk per trade
- Max daily loss
- Warning when rules are violated

### 🌍 Realism (Optional)
- Spread input
- Slippage buffer
- Commission model

---

## 🧘 Final Note

This app is not about prediction.  
It’s about **survival, consistency, and honesty**.

If a trade doesn’t look good *here*, it won’t magically look better in the market.
