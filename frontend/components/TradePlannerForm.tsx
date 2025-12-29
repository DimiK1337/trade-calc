"use client";

import { useMemo, useState } from "react";
import { Box, Button, Input, SimpleGrid, Stack, Text } from "@chakra-ui/react";

import type { CalcInputs, CalcResult, SymbolKey } from "@/lib/types";
import type { Direction } from "@/lib/defaults/tradePlanner";
import { computePositionSize } from "@/lib/calc";
import { computeSLTP } from "@/lib/tradePlanner";
import { DEFAULT_TRADE_PLANNER } from "@/lib/defaults/tradePlanner";


import Results from "@/components/Results";
import GoldFields from "@/components/GoldFields";
import FxFields from "@/components/FxFields";

interface TradePlannerFormState extends CalcInputs {
  direction: Direction;
  entryPrice: number;
  rewardToRisk: number;
}

const DEFAULTS = DEFAULT_TRADE_PLANNER;


export default function TradePlannerForm() {
  const [inputs, setInputs] = useState<TradePlannerFormState>(DEFAULTS);
  const [sizeResult, setSizeResult] = useState<CalcResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const isGold = inputs.symbol === "XAUUSD";
  const stopLabel = useMemo(
    () => (isGold ? "Stop distance (ticks)" : "Stop distance (pips)"),
    [isGold]
  );

  function update<K extends keyof TradePlannerFormState>(key: K, value: TradePlannerFormState[K]) {
    setInputs((prev) => ({ ...prev, [key]: value }));
  }

  const plan = useMemo(() => {
    try {
      return computeSLTP({
        symbol: inputs.symbol,
        direction: inputs.direction,
        entryPrice: inputs.entryPrice,
        stopDistance: inputs.stopDistance,
        rewardToRisk: inputs.rewardToRisk,
      });
    } catch {
      return null;
    }
  }, [
    inputs.symbol,
    inputs.direction,
    inputs.entryPrice,
    inputs.stopDistance,
    inputs.rewardToRisk,
  ]);

  const planError = useMemo(() => {
    try {
      computeSLTP({
        symbol: inputs.symbol,
        direction: inputs.direction,
        entryPrice: inputs.entryPrice,
        stopDistance: inputs.stopDistance,
        rewardToRisk: inputs.rewardToRisk,
      });
      return null;
    } catch (e) {
      return e instanceof Error ? e.message : "Invalid trade plan inputs.";
    }
  }, [
    inputs.symbol,
    inputs.direction,
    inputs.entryPrice,
    inputs.stopDistance,
    inputs.rewardToRisk,
  ]);


  function calculate() {
    setError(null);
    setSizeResult(null);

    if (planError) {
      setError(planError);
      return;
    }

    try {
      const r = computePositionSize(inputs);
      setSizeResult(r);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Calculation failed.");
    }
  }


  // Derived CHF reward at TP (approx, using your value-per-unit model)
  const rewardCHF = useMemo(() => {
    if (!sizeResult) return null;
    if (!plan) return null;

    // Convert rewardDistancePrice back into units (pips/ticks) to reuse valuePerUnitPerLot
    const unitSize =
      inputs.symbol === "XAUUSD"
        ? inputs.goldTickSize // tick size
        : (inputs.symbol.endsWith("JPY") ? 0.01 : 0.0001); // pip size

    const rewardUnits = plan.rewardDistancePrice / unitSize; // ticks or pips
    const rewardPerLotCHF = rewardUnits * sizeResult.valuePerUnitPerLotCHF;
    const totalRewardCHF = rewardPerLotCHF * sizeResult.lots;

    return totalRewardCHF;
  }, [sizeResult, plan, inputs.symbol, inputs.goldTickSize]);

  return (
    <Stack gap={4}>
      <Box borderWidth="1px" rounded="xl" p={5}>
        <Stack gap={4}>
          <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
            <Field label="Balance (CHF)">
              <Input
                type="number"
                value={inputs.balance}
                onChange={(e) => update("balance", Number(e.target.value))}
              />
            </Field>

            <Field label="Risk (% per trade)">
              <Input
                type="number"
                step="0.1"
                value={inputs.riskPct}
                onChange={(e) => update("riskPct", Number(e.target.value))}
              />
            </Field>

            <Field label="Direction">
              <select
                value={inputs.direction}
                onChange={(e) => update("direction", e.target.value as Direction)}
                style={{
                  width: "100%",
                  padding: "8px 12px",
                  borderRadius: "6px",
                  border: "1px solid rgba(255,255,255,0.2)",
                  background: "transparent",
                  color: "inherit",
                }}
              >
                <option value="LONG">LONG</option>
                <option value="SHORT">SHORT</option>
              </select>
            </Field>


            <Field label="Entry price">
              <Input
                type="number"
                value={inputs.entryPrice}
                onChange={(e) => update("entryPrice", Number(e.target.value))}
              />
            </Field>

            <Field label="Symbol">
              <select
                value={inputs.symbol}
                onChange={(e) => update("symbol", e.target.value as SymbolKey)}
                style={{
                  width: "100%",
                  padding: "8px 12px",
                  borderRadius: "6px",
                  border: "1px solid rgba(255,255,255,0.2)",
                  background: "transparent",
                  color: "inherit",
                }}
              >
                <option value="XAUUSD">XAUUSD (Gold)</option>
                <option value="EURUSD">EURUSD</option>
                <option value="USDCHF">USDCHF</option>
                <option value="USDJPY">USDJPY</option>
              </select>
            </Field>

            <Field label={stopLabel}>
              <Input
                type="number"
                value={inputs.stopDistance}
                onChange={(e) => update("stopDistance", Number(e.target.value))}
              />
            </Field>

            <Field label="TP as R-multiple (reward to risk (reward = 2*Risk)) (e.g. 2 = 2R)">
              <Input
                type="number"
                step="0.25"
                value={inputs.rewardToRisk}
                onChange={(e) => update("rewardToRisk", Number(e.target.value))}
              />
            </Field>

            <Field label="Lot step">
              <Input
                type="number"
                step="0.01"
                value={inputs.lotStep}
                onChange={(e) => update("lotStep", Number(e.target.value))}
              />
            </Field>
          </SimpleGrid>

          <Separator />

          {isGold ? (
            <GoldFields
              goldContractSize={inputs.goldContractSize}
              goldTickSize={inputs.goldTickSize}
              usdchfRate={inputs.usdchfRate}
              onChange={(patch) => setInputs((prev) => ({ ...prev, ...patch }))}
            />
          ) : (
            <FxFields
              symbol={inputs.symbol}
              usdchfRate={inputs.usdchfRate}
              onChange={(patch) => setInputs((prev) => ({ ...prev, ...patch }))}
            />
          )}

          <Separator />

          <Button onClick={calculate}>Calculate size + plan</Button>

          {error && (
            <Box borderWidth="1px" borderColor="red.400" rounded="lg" p={3}>
              <Text fontSize="sm">{error}</Text>
            </Box>
          )}

          {/* Show SL/TP plan */}
          <Box borderWidth="1px" rounded="xl" p={5}>
            <Text fontWeight="medium" mb={2}>
              Plan
            </Text>

            {plan ? (
              <Stack gap={1}>
                <Row label="SL price">{plan.slPrice.toFixed(isGold ? 2 : 5)}</Row>
                <Row label="TP price">{plan.tpPrice.toFixed(isGold ? 2 : 5)}</Row>
                <Row label="Risk distance (price)">{plan.riskDistancePrice.toString()}</Row>
                <Row label="Reward distance (price)">{plan.rewardDistancePrice.toString()}</Row>
                {sizeResult && rewardCHF != null && (
                  <Row label="Reward at TP (CHF, approx)">{rewardCHF.toFixed(2)}</Row>
                )}
              </Stack>
            ) : (
              <Text opacity={0.7}>Fill entry/stop/R to compute SL/TP.</Text>
            )}
          </Box>

          {/* Reuse your existing Results component for sizing */}
          <Results symbol={inputs.symbol} result={sizeResult} />

          <Text fontSize="xs" opacity={0.7}>
            Planner TP uses R-multiple. For XAUUSD it assumes tick size 0.01 unless you pass a different tick size
            (we’re using your goldTickSize for reward calc).
          </Text>
        </Stack>
      </Box>
    </Stack>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <Box>
      <Text fontSize="sm" mb={1} opacity={0.8}>
        {label}
      </Text>
      {children}
    </Box>
  );
}

function Separator() {
  return <Box h="1px" bg="whiteAlpha.300" />;
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <Box display="flex" justifyContent="space-between" gap={4}>
      <Text opacity={0.75}>{label}</Text>
      <Text fontFamily="mono">{children}</Text>
    </Box>
  );
}
