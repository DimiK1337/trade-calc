import { api, TOKEN_KEY } from "./client";

export type UserOut = {
  id: number;
  email: string;
  username: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};

// ---------- API calls ----------

export async function registerUser(params: {
  email: string;
  username: string;
  password: string;
}): Promise<UserOut> {
  const res = await api.post<UserOut>("/api/v1/auth/register", params);
  return res.data;
}

export async function loginUser(params: {
  identifier: string; // email or username
  password: string;
}): Promise<TokenResponse> {
  const body = new URLSearchParams();
  body.set("username", params.identifier); // OAuth2 naming
  body.set("password", params.password);

  const res = await api.post<TokenResponse>(
    "/api/v1/auth/token",
    body,
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
  );
  return res.data;
}

export async function fetchMe(): Promise<UserOut> {
  const res = await api.get<UserOut>("/api/v1/auth/me");
  return res.data;
}

// ---------- helpers ----------

export function storeToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function initialsFromUser(user: {
  email: string;
  username: string;
}) {
  const u = user.username?.trim();
  if (u && u.length >= 2) return u.slice(0, 2).toUpperCase();
  if (u && u.length === 1) return u.toUpperCase();

  const e = user.email?.split("@")[0] ?? "";
  if (e.length >= 2) return e.slice(0, 2).toUpperCase();
  if (e.length === 1) return e.toUpperCase();

  return "U";
}

export function colorFromString(input: string) {
  let hash = 0;
  for (let i = 0; i < input.length; i++) {
    hash = (hash * 31 + input.charCodeAt(i)) >>> 0;
  }
  const hue = hash % 360;
  return `hsl(${hue} 60% 45%)`;
}
