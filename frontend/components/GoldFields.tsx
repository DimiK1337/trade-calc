"use client";

import { Box, Input, SimpleGrid, Stack, Text } from "@chakra-ui/react";
import type { CalcInputs } from "../lib/types";

interface GoldFieldsProps {
  goldContractSize: number;
  goldTickSize: number;
  usdchfRate: number;
  onChange: (patch: Partial<CalcInputs>) => void;
}

export default function GoldFields(props: GoldFieldsProps) {
  return (
    <Stack gap={3}>
      <Text fontWeight="medium">Gold Settings (XAUUSD)</Text>

      <SimpleGrid columns={{ base: 1, md: 3 }} gap={4}>
        <Field label="Contract size (oz per 1.0 lot)">
          <Input
            type="number"
            value={props.goldContractSize}
            onChange={(e) =>
              props.onChange({ goldContractSize: Number(e.target.value) })
            }
          />
        </Field>

        <Field label="Tick size">
          <Input
            type="number"
            step="0.01"
            value={props.goldTickSize}
            onChange={(e) => props.onChange({ goldTickSize: Number(e.target.value) })}
          />
        </Field>

        <Field label="USD→CHF rate (USDCHF)">
          <Input
            type="number"
            step="0.0001"
            value={props.usdchfRate}
            onChange={(e) => props.onChange({ usdchfRate: Number(e.target.value) })}
          />
        </Field>
      </SimpleGrid>
    </Stack>
  );
}

function Field(props: { label: string; children: React.ReactNode }) {
  return (
    <Box>
      <Text fontSize="sm" mb={1} opacity={0.8}>
        {props.label}
      </Text>
      {props.children}
    </Box>
  );
}
