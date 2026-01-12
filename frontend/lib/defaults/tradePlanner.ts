// lib/defaults/tradePlanner.ts

import type { CalcInputs } from "../types";

export type Direction = "LONG" | "SHORT";

export interface TradePlannerDefaults extends CalcInputs {
  direction: Direction;
  entryPrice: number;
  rewardToRisk: number; // reward / risk (e.g., 2 means target profit is 2× risk)
}

import { DEFAULT_CALC_INPUTS } from "./base";

/**
 * Defaults for the /trade-planner route.
 */
export const DEFAULT_TRADE_PLANNER: TradePlannerDefaults = {
  ...DEFAULT_CALC_INPUTS,
  direction: "LONG",
  entryPrice: 2650,
  rewardToRisk: 2,
};
