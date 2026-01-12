// lib/defaults/calculator.ts

import type { CalcInputs } from "../types";
import { DEFAULT_CALC_INPUTS } from "./base";

/**
 * Defaults for the /calculator route.
 * Right now this is identical to the shared base, but keeping it separate
 * lets you later customize calculator-specific defaults without affecting other routes.
 */
export const DEFAULT_CALCULATOR: CalcInputs = {
  ...DEFAULT_CALC_INPUTS,
};
