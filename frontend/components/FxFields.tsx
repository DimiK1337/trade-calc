"use client";

import type { CalcInputs } from "@/lib/types";

import { Box, 
  Input, 
  SimpleGrid, 
  Stack, 
  Text 
} from "@chakra-ui/react";

interface FxFieldsProps {
  symbol: CalcInputs["symbol"];
  usdchfRate: number;
  onChange: (patch: Partial<CalcInputs>) => void;
}

export default function FxFields(props: FxFieldsProps) {
  const needsUsdChf = props.symbol !== "USDCHF";

  return (
    <Stack gap={3}>
      <Text fontWeight="medium">FX Settings</Text>

      <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
        <Field label="USD→CHF rate (USDCHF)" disabled={!needsUsdChf}>
          <Input
            type="number"
            step="0.0001"
            value={props.usdchfRate}
            onChange={(e) =>
              props.onChange({ usdchfRate: Number(e.target.value) })
            }
            disabled={!needsUsdChf}
          />
        </Field>

        <Text fontSize="sm" opacity={0.75} alignSelf="end">
          USDCHF is only needed when the quote currency isn’t CHF (e.g., EURUSD).
        </Text>
      </SimpleGrid>
    </Stack>
  );
}

function Field(props: {
  label: string;
  disabled?: boolean;
  children: React.ReactNode;
}) {
  return (
    <Box opacity={props.disabled ? 0.6 : 1}>
      <Text fontSize="sm" mb={1} opacity={0.8}>
        {props.label}
      </Text>
      {props.children}
    </Box>
  );
}
