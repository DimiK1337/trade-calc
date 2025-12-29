import type { CalcInputs } from "../types";

export function validateInputs(input: CalcInputs) {
  const {
    accountCcy,
    balance,
    riskPct,
    stopDistance,
    lotStep,
    usdchfRate,
  } = input;

  if (accountCcy !== "CHF") throw new Error("MVP: only CHF accounts supported.");
  if (!(balance > 0)) throw new Error("Balance must be > 0.");
  if (!(riskPct > 0 && riskPct <= 5)) throw new Error("Risk % must be between 0 and 5.");
  if (!(stopDistance > 0)) throw new Error("Stop distance must be > 0.");
  if (!(lotStep > 0)) throw new Error("Lot step must be > 0.");
  if (!(usdchfRate > 0)) throw new Error("USD→CHF rate must be > 0.");
}
