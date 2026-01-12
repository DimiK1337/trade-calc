// lib/trades/index.ts
import { api } from "@/lib/auth/client";

export type StopUnit = "TICKS" | "PIPS";
export type TradeDirection = "LONG" | "SHORT";
export type TradeStatus = "PLANNED" | "OPEN" | "CLOSED" | "CANCELLED";

export type TradeInputs = {
  balance_chf?: number | null;
  risk_pct?: number | null;

  symbol: string;
  direction: TradeDirection;
  entry_price: number;

  stop_distance: number;
  stop_unit: StopUnit;

  tp_r_multiple?: number | null;
  lot_step?: number | null;

  usdchf_rate?: number | null;
  tick_size?: number | null;
  contract_size?: number | null;
};

export type TradeOutputs = {
  sl_price: number;
  tp_price: number;

  risk_distance_price?: number | null;
  reward_distance_price?: number | null;

  lots: number;
  risk_chf: number;
  reward_chf: number;
  reward_to_risk: number;

  value_per_unit_1lot_chf?: number | null;
  stop_value_1lot_chf?: number | null;
  exposure_units?: number | null;
};

export type TradeJournal = {
  note?: string | null;
  status: TradeStatus;

  opened_at?: string | null;
  closed_at?: string | null;

  realized_pnl_chf?: number | null;
  realized_r_multiple?: number | null;
};

export type TradeCreate = {
  inputs: TradeInputs;
  outputs: TradeOutputs;
  journal: TradeJournal;
};

export type TradeDetailOut = {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  inputs: TradeInputs;
  outputs: TradeOutputs;
  journal: TradeJournal;
};

export async function createTrade(payload: TradeCreate): Promise<TradeDetailOut> {
  const res = await api.post("/api/v1/trades", payload);
  return res.data;
}

type FastApiErrorDetail =
  | string
  | Array<{
      loc?: unknown;
      msg?: unknown;
    }>;

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

export function extractFastApiError(e: unknown): string {
  if (!isObject(e)) {
    return "Request failed";
  }

  const response = e["response"];
  if (!isObject(response)) {
    return "Request failed";
  }

  const data = response["data"];
  if (!isObject(data)) {
    return "Request failed";
  }

  const detail = data["detail"] as FastApiErrorDetail | undefined;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (!isObject(item)) return "Invalid value";

        const loc =
          Array.isArray(item["loc"])
            ? item["loc"].map(String).join(".")
            : "validation";

        const msg = typeof item["msg"] === "string" ? item["msg"] : "Invalid value";

        return `${loc}: ${msg}`;
      })
      .join("\n");
  }

  return "Request failed";
}

