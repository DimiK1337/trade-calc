// lib/defaults/base.ts

import type { CalcInputs } from "../types";

/**
 * Shared defaults used across forms (Calculator, Trade Planner, later Journal, etc.)
 * Keep this as the single source of truth for "account + instrument sizing" defaults.
 */
export const DEFAULT_CALC_INPUTS: CalcInputs = {
  accountCcy: "CHF",
  balance: 5000,
  riskPct: 0.5,
  symbol: "XAUUSD",
  stopDistance: 20,
  usdchfRate: 0.9,
  lotStep: 0.01,
  goldContractSize: 100,
  goldTickSize: 0.01,
};
