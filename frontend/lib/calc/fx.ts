import type { SymbolKey } from "../types";

const FX_CONTRACT_SIZE = 100_000;

function pipSize(symbol: SymbolKey): number {
  return symbol.endsWith("JPY") ? 0.01 : 0.0001;
}

export function fxValuePerPipPerLotCHF(
  symbol: SymbolKey,
  usdchfRate: number
): number {
  const ps = pipSize(symbol);

  if (symbol.endsWith("CHF")) {
    return FX_CONTRACT_SIZE * ps;
  }

  // MVP approximation for EURUSD / USDJPY
  const pipValueUSD = FX_CONTRACT_SIZE * ps;
  return pipValueUSD * usdchfRate;
}

export function fxExposureUnits(lots: number): number {
  return Math.round(lots * FX_CONTRACT_SIZE);
}
