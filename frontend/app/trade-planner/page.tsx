import { Box, Heading, Text } from "@chakra-ui/react";
import TradePlannerForm from "@/components/TradePlannerForm";

export const metadata = { title: "Trade Planner" };

export default function TradePlannerPage() {
  return (
    <Box maxW="3xl" mx="auto" px={6} py={8}>
      <Heading size="lg">Trade Planner</Heading>
      <Text mt={2} opacity={0.8}>
        Plan Entry + SL + TP using an R-multiple, and compute position size + CHF risk/reward.
      </Text>

      <Box mt={6}>
        <TradePlannerForm />
      </Box>
    </Box>
  );
}
