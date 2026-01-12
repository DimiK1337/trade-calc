// lib/types.tsx

export type SymbolKey = "XAUUSD" | "EURUSD" | "USDCHF" | "USDJPY";

export type CalcInputs = {
  accountCcy: "CHF"; // MVP constraint (we’ll generalize later)
  balance: number;
  riskPct: number; // e.g. 0.5
  symbol: SymbolKey;

  // Stop distance meaning:
  // - FX: pips
  // - XAUUSD: ticks
  stopDistance: number;

  // Conversion (MVP)
  usdchfRate: number; // USD -> CHF

  // Rounding
  lotStep: number; // e.g. 0.01

  // XAUUSD specs (editable; broker-dependent)
  goldContractSize: number; // oz per 1.0 lot (common: 100)
  goldTickSize: number; // common: 0.01
};

export type CalcResult = {
  riskMoneyCHF: number;
  valuePerUnitPerLotCHF: number; // CHF per pip (FX) or tick (XAUUSD) per 1.0 lot
  stopValuePerLotCHF: number; // CHF loss per 1.0 lot if stop hit (ignores spread/fees)
  lots: number; // rounded down
  exposureUnits: number; // approx units (FX) or oz (gold)
  unitLabel: string; // "units" or "oz"
  distanceLabel: string; // "pips" or "ticks"
};
