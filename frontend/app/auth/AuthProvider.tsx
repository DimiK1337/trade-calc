"use client";

import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import {
  fetchMe,
  loginUser,
  registerUser,
  storeToken,
  clearToken,
  getToken,
  type UserOut,
} from "@/lib/auth";

type AuthContextValue = {
  user: UserOut | null;
  isLoading: boolean;
  login: (params: { identifier: string; password: string }) => Promise<void>;
  register: (params: { email: string; username: string; password: string }) => Promise<void>;
  logout: () => void;
  refreshMe: () => Promise<void>; // TODO: This is for MVP, in prod shouldn't have to send an extra request to view updates on UI
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserOut | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initial session restore
  useEffect(() => {
    let cancelled = false;

    async function restore() {
      const token = getToken();
      if (!token) {
        if (!cancelled) setIsLoading(false);
        return;
      }

      try {
        const me = await fetchMe();
        if (!cancelled) setUser(me);
      } catch {
        clearToken();
        if (!cancelled) setUser(null);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    restore();
    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (params: { identifier: string; password: string }) => {
    const token = await loginUser(params);
    storeToken(token.access_token);
    const me = await fetchMe();
    setUser(me);
  }, []);

  const register = useCallback(async (params: { email: string; username: string; password: string }) => {
    await registerUser(params);
    // Email precedence for identifier:
    const token = await loginUser({ identifier: params.email, password: params.password });
    storeToken(token.access_token);
    const me = await fetchMe();
    setUser(me);
  }, []);

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
  }, []);

  const refreshMe = useCallback(async () => {
    const token = getToken();
    if (!token) {
      setUser(null);
      return;
    }
    const me = await fetchMe();
    setUser(me);
  }, []);


  const value = useMemo(
    () => ({ user, isLoading, login, register, logout, refreshMe }),
    [user, isLoading, login, register, logout, refreshMe]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
