"use client";

import { Box, Heading, Text } from "@chakra-ui/react";
import type { CalcResult, SymbolKey } from "../lib/types";

interface ResultsProps {
  symbol: SymbolKey;
  result: CalcResult | null;
}

export default function Results({ symbol, result }: ResultsProps) {
  if (!result) {
    return (
      <Panel>
        <Text opacity={0.7}>No result yet. Fill the inputs and click Calculate.</Text>
      </Panel>
    );
  }

  const unitWord = symbol === "XAUUSD" ? "tick" : "pip";

  return (
    <Panel>
      <Heading size="sm" mb={3}>
        Result
      </Heading>

      <Row label="Risk money">{result.riskMoneyCHF.toFixed(2)} CHF</Row>
      <Row label={`Value per ${unitWord} (1.0 lot)`}>
        {result.valuePerUnitPerLotCHF.toFixed(4)} CHF
      </Row>
      <Row label="Stop value (1.0 lot)">{result.stopValuePerLotCHF.toFixed(2)} CHF</Row>
      <Row label="Lot size">{result.lots.toFixed(2)} lots</Row>
      <Row label={`Exposure (${result.unitLabel})`}>{result.exposureUnits.toLocaleString()}</Row>

      <Text mt={3} fontSize="xs" opacity={0.7}>
        Assumes stop loss is executed exactly at the stop price (no slippage) and ignores spread/fees.
      </Text>
    </Panel>
  );
}

function Panel({ children }: { children: React.ReactNode }) {
  return (
    <Box borderWidth="1px" rounded="xl" p={5}>
      {children}
    </Box>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <Box display="flex" justifyContent="space-between" gap={4} mb={1}>
      <Text opacity={0.75}>{label}</Text>
      <Text fontFamily="mono">{children}</Text>
    </Box>
  );
}
