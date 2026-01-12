// lib/tradePlanner/index.ts

import type { CalcInputs, SymbolKey } from "@/lib/types";

import type { Direction } from "@/lib/defaults/tradePlanner";

function pipSize(symbol: SymbolKey): number {
  return symbol.endsWith("JPY") ? 0.01 : 0.0001;
}

export type TradePlanInputs = {
  direction: Direction;
  entryPrice: number;
  rewardToRisk: number; // e.g. 2 means TP at 2R
} & Pick<CalcInputs, "symbol" | "stopDistance">;

export type TradePlanResult = {
  slPrice: number;
  tpPrice: number;
  riskDistancePrice: number; // |entry - SL|
  rewardDistancePrice: number; // |TP - entry|
};

export function computeSLTP(input: TradePlanInputs): TradePlanResult {
  const { symbol, direction, entryPrice, stopDistance, rewardToRisk } = input;

  if (!(entryPrice > 0)) throw new Error("Entry price must be > 0.");
  if (!(stopDistance > 0)) throw new Error("Stop distance must be > 0.");
  if (!(rewardToRisk > 0)) throw new Error("R multiple must be > 0.");

  // Convert stopDistance (pips/ticks) into a price delta:
  let step: number;
  if (symbol === "XAUUSD") {
    // In your sizing model, stopDistance for gold is "ticks".
    // tick size is broker-dependent; we’ll assume 0.01 for planning unless you later pass it in.
    // For consistency, you can later pass goldTickSize into planner inputs.
    step = 0.01;
  } else {
    // FX: pips -> price
    step = pipSize(symbol);
  }

  const riskDistancePrice = stopDistance * step;
  const rewardDistancePrice = riskDistancePrice * rewardToRisk;

  const slPrice =
    direction === "LONG" ? entryPrice - riskDistancePrice : entryPrice + riskDistancePrice;

  const tpPrice =
    direction === "LONG" ? entryPrice + rewardDistancePrice : entryPrice - rewardDistancePrice;

  return { slPrice, tpPrice, riskDistancePrice, rewardDistancePrice };
}
