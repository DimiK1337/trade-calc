// lib/auth/client.ts

import axios from "axios";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 10_000,
  headers: {
    "Content-Type": "application/json",
  },
});

const TOKEN_KEY = "tradecalc_token_v1";

// Attach token automatically
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Global auth failure handling
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err?.response?.status === 401 && typeof window !== "undefined") {
      // Token invalid / expired
      localStorage.removeItem(TOKEN_KEY);
      // No redirect here — let UI decide
    }
    return Promise.reject(err);
  }
);

export { TOKEN_KEY };
