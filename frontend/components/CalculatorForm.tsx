"use client";

import React from "react";
import { useMemo, useState } from "react";
import {
  Box,
  Button,
  ButtonGroup,
  Input,
  SimpleGrid,
  Stack,
  Text,
} from "@chakra-ui/react";

import type { CalcInputs, CalcResult, SymbolKey } from "@/lib/types";
import { computePositionSize } from "@/lib/calc";
import FxFields from "@/components/FxFields";
import GoldFields from "@/components/GoldFields";
import Results from "@/components/Results";
import { DEFAULT_CALCULATOR } from "@/lib/defaults/calculator";

const DEFAULTS = DEFAULT_CALCULATOR

export default function CalculatorForm() {
  const [inputs, setInputs] = useState<CalcInputs>(DEFAULTS);
  const [result, setResult] = useState<CalcResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const isGold = inputs.symbol === "XAUUSD";

  const stopLabel = useMemo(
    () => (isGold ? "Stop distance (ticks)" : "Stop distance (pips)"),
    [isGold]
  );

  function update<K extends keyof CalcInputs>(key: K, value: CalcInputs[K]) {
    setInputs((prev) => ({ ...prev, [key]: value }));
  }

  function calculate() {
    setError(null);
    setResult(null);
    try {
      const r = computePositionSize(inputs);
      setResult(r);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Calculation failed.");
    }
  }

  return (
    <Stack gap={4}>
      <Box borderWidth="1px" rounded="xl" p={5}>
        <Stack gap={4}>
          {/* Account + instrument */}
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
                {/* TODO: Make this an iterable and loop over */}
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

          <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
            <Field label="Lot step">
              <Input
                type="number"
                step="0.01"
                value={inputs.lotStep}
                onChange={(e) => update("lotStep", Number(e.target.value))}
              />
            </Field>

            <Field label="Account currency (MVP)">
              <Input value={inputs.accountCcy} readOnly />
            </Field>
          </SimpleGrid>

          <ButtonGroup flexWrap={"wrap"}>
            <Button onClick={calculate}>Calculate</Button>
            <Button variant="outline" onClick={() => update("riskPct", 0.25)}>
              0.25%
            </Button>
            <Button variant="outline" onClick={() => update("riskPct", 0.5)}>
              0.5%
            </Button>
            <Button variant="outline" onClick={() => update("riskPct", 1)}>
              1%
            </Button>
            <Button
              variant="ghost"
              onClick={() => {
                setInputs(DEFAULTS);
                setResult(null);
                setError(null);
              }}
            >
              Reset
            </Button>
          </ButtonGroup>

          {error && (
            <Box borderWidth="1px" borderColor="red.400" rounded="lg" p={3}>
              <Text fontSize="sm">{error}</Text>
            </Box>
          )}

          <Results symbol={inputs.symbol} result={result} />

          <Text fontSize="xs" opacity={0.7}>
            XAUUSD specs vary by broker. Verify contract & tick size in MT5.
            USDJPY pip value is approximated in this MVP.
          </Text>
        </Stack>
      </Box>
    </Stack>
  );
}

function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
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
