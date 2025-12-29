export function goldValuePerTickPerLotCHF(
  contractSize: number,
  tickSize: number,
  usdchfRate: number
): number {
  if (!(contractSize > 0)) throw new Error("Gold contract size must be > 0.");
  if (!(tickSize > 0)) throw new Error("Gold tick size must be > 0.");

  const tickValueUSD = contractSize * tickSize;
  return tickValueUSD * usdchfRate;
}

export function goldExposureOz(lots: number, contractSize: number): number {
  return Math.round(lots * contractSize);
}
