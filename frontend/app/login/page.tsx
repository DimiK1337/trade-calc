"use client";

import { useState } from "react";
import NextLink from "next/link";
import { Box, Button, Heading, Input, Text } from "@chakra-ui/react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/app/auth/AuthProvider";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();

  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);

    const id = identifier.trim();
    if (!id || !password) {
      setError("Enter your email/username and password.");
      return;
    }

    setBusy(true);
    try {
      await login({ identifier: id, password });
      router.push("/calculator");
    } catch (err: unknown) {
      setError(extractErrorMessage(err, "Login failed"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <Box maxW="md" mx="auto" px={6} py={10}>
      <Heading size="lg" mb={2}>
        Login
      </Heading>
      <Text opacity={0.8} mb={6}>
        Use your email or username.
      </Text>

      <form onSubmit={onSubmit} noValidate>
        <Box borderWidth="1px" rounded="xl" p={6} >
          <Field label="Email or username">
            <Input
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              autoComplete="username"
              placeholder="name@example.com or username"
            />
          </Field>

          <Field label="Password">
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              placeholder="••••••••"
            />
          </Field>

          {error && (
            <Box mt={3} p={3} borderWidth="1px" rounded="md">
              <Text fontSize="sm">{error}</Text>
            </Box>
          )}

          <Button mt={4} type="submit" width="100%" disabled={busy}>
            {busy ? "Logging in..." : "Login"}
          </Button>

          <Text mt={4} fontSize="sm" opacity={0.8}>
            No account?{" "}
            <NextLink href="/register" style={{ textDecoration: "underline" }}>
              Register
            </NextLink>
          </Text>
        </Box>
      </form>
    </Box>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <Box mb={4}>
      <Text mb={2} fontSize="sm" opacity={0.8}>
        {label}
      </Text>
      {children}
    </Box>
  );
}

type AxiosishError = {
  response?: {
    data?: unknown;
    status?: number;
  };
  message?: string;
};

function extractErrorMessage(err: unknown, fallback: string): string {
  if (err instanceof Error) return err.message;

  const e = err as AxiosishError;
  const data = e?.response?.data;

  // FastAPI often returns { detail: "..." } or { detail: [...] }
  if (data && typeof data === "object" && "detail" in data) {
    const detail = (data as { detail: unknown }).detail;
    if (typeof detail === "string") return detail;
    return JSON.stringify(detail);
  }

  if (typeof data === "string") return data;
  if (typeof e?.message === "string") return e.message;

  return fallback;
}
