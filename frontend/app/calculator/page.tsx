import { Box, Heading, Text } from "@chakra-ui/react";
import CalculatorForm from "../../components/CalculatorForm"

export const metadata = {
  title: "Calculator",
};

export default function CalculatorPage() {
  return (
    <Box maxW="3xl" mx="auto" px={6} py={8}>
      <Heading size="lg">Position Size Calculator</Heading>

      <Text mt={2} opacity={0.8}>
        Enter balance, risk %, and stop distance. This returns a lot size that targets your
        risk budget (ignores slippage/spread for now).
      </Text>

      <Box mt={6}>
        <CalculatorForm />
      </Box>
    </Box>
  );
}
