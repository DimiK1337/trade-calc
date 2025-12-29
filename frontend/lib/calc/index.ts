import type { CalcInputs, CalcResult } from "../types";
import { validateInputs } from "./validate";
import { fxValuePerPipPerLotCHF, fxExposureUnits } from "./fx";
import { goldValuePerTickPerLotCHF, goldExposureOz } from "./gold";

function roundDownToStep(value: number, step: number): number {
  const inv = 1 / step;
  return Math.floor(value * inv) / inv;
}

export function computePositionSize(input: CalcInputs): CalcResult {
  validateInputs(input);

  const riskMoneyCHF = input.balance * (input.riskPct / 100);

  let valuePerUnitPerLotCHF: number;
  let exposureUnits: number;
  let unitLabel: string;
  let distanceLabel: string;

  if (input.symbol === "XAUUSD") {
    valuePerUnitPerLotCHF = goldValuePerTickPerLotCHF(
      input.goldContractSize,
      input.goldTickSize,
      input.usdchfRate
    );
    exposureUnits = goldExposureOz(0, 0); // placeholder, see below
    unitLabel = "oz";
    distanceLabel = "ticks";
  } else {
    valuePerUnitPerLotCHF = fxValuePerPipPerLotCHF(
      input.symbol,
      input.usdchfRate
    );
    unitLabel = "units";
    distanceLabel = "pips";
  }

  const stopValuePerLotCHF = input.stopDistance * valuePerUnitPerLotCHF;
  const rawLots = riskMoneyCHF / stopValuePerLotCHF;
  const lots = roundDownToStep(rawLots, input.lotStep);

  if (!(lots > 0)) {
    throw new Error("Lot size rounded down to 0.");
  }

  if (input.symbol === "XAUUSD") {
    exposureUnits = goldExposureOz(lots, input.goldContractSize);
  } else {
    exposureUnits = fxExposureUnits(lots);
  }

  return {
    riskMoneyCHF,
    valuePerUnitPerLotCHF,
    stopValuePerLotCHF,
    lots,
    exposureUnits,
    unitLabel,
    distanceLabel,
  };
}
