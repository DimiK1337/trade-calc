"use client";

import { useMemo, useState } from "react";
import { Box, Button, Heading, Input, Text } from "@chakra-ui/react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/app/auth/AuthProvider";
import {
  updateProfile,
  changeMyPassword,
  deleteMyAccount,
} from "@/lib/auth";

export default function ProfilePage() {
  const router = useRouter();
  const { user, isLoading, logout, refreshMe } = useAuth();

  // Form state
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const [emailPassword, setEmailPassword] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const [deletePassword, setDeletePassword] = useState("");
  const [deleteConfirm, setDeleteConfirm] = useState("");

  const [busy, setBusy] = useState<null | "username" | "email" | "password" | "delete">(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const canDelete = useMemo(() => {
    return deletePassword.trim().length > 0 && deleteConfirm.trim() === "DELETE";
  }, [deletePassword, deleteConfirm]);

  // Initialize input defaults once user loads (without fighting controlled inputs)
  // If you want it to auto-fill, we’ll do it only when user changes from null->value.
  const initialValues = useMemo(() => {
    if (!user) return null;
    return { username: user.username, email: user.email };
  }, [user]);

  // If user is still loading, show placeholder.
  if (isLoading) {
    return (
      <Box maxW="3xl" mx="auto" px={6} py={10}>
        <Heading size="lg">Profile</Heading>
        <Text mt={3} opacity={0.7}>Loading…</Text>
      </Box>
    );
  }

  // Not logged in => redirect-ish UX
  if (!user) {
    return (
      <Box maxW="3xl" mx="auto" px={6} py={10}>
        <Heading size="lg">Profile</Heading>
        <Text mt={3} opacity={0.8}>
          You need to be logged in to view this page.
        </Text>
        <Button mt={4} onClick={() => router.push("/login")}>
          Go to Login
        </Button>
      </Box>
    );
  }

  const existingUser = user;

  // Set default placeholders (not force-writing state)
  const shownUsername = username || initialValues?.username || "";
  const shownEmail = email || initialValues?.email || "";

  async function submitUsername(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setNotice(null);
    setError(null);

    const next = username.trim();
    if (!next) {
      setError("Username cannot be empty.");
      return;
    }
    if (next === existingUser.username) {
      setNotice("No change.");
      return;
    }

    setBusy("username");
    try {
      await updateProfile({ username: next });
      setNotice("Username updated.");
      setUsername(""); // reset input
      await refreshMe();
    } catch (err: unknown) {
      setError(extractErrorMessage(err, "Failed to update username"));
    } finally {
      setBusy(null);
    }
  }

  async function submitEmail(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setNotice(null);
    setError(null);

    const next = email.trim();
    if (!next) {
      setError("Email cannot be empty.");
      return;
    }
    if (next === existingUser.email) {
      setNotice("No change.");
      return;
    }
    if (!emailPassword) {
      setError("Current password is required to change email.");
      return;
    }

    setBusy("email");
    try {
      await updateProfile({ email: next, current_password: emailPassword });
      setNotice("Email updated.");
      setEmail("");
      setEmailPassword("");
      await refreshMe();
    } catch (err: unknown) {
      setError(extractErrorMessage(err, "Failed to update email"));
    } finally {
      setBusy(null);
    }
  }

  async function submitPassword(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setNotice(null);
    setError(null);

    if (!currentPassword || !newPassword) {
      setError("Provide current password and new password.");
      return;
    }
    if (newPassword.length < 8) {
      setError("New password must be at least 8 characters.");
      return;
    }

    setBusy("password");
    try {
      await changeMyPassword({
        current_password: currentPassword,
        new_password: newPassword,
      });
      setNotice("Password updated. Please log in again.");
      setCurrentPassword("");
      setNewPassword("");
      logout();
      router.push("/login");
    } catch (err: unknown) {
      setError(extractErrorMessage(err, "Failed to change password"));
    } finally {
      setBusy(null);
    }
  }

  async function submitDelete(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setNotice(null);
    setError(null);

    if (!canDelete) {
      setError('To delete your account: enter password + type "DELETE".');
      return;
    }

    setBusy("delete");
    try {
      await deleteMyAccount({ current_password: deletePassword });
      setNotice("Account deleted.");
      logout();
      router.push("/register");
    } catch (err: unknown) {
      setError(extractErrorMessage(err, "Failed to delete account"));
    } finally {
      setBusy(null);
    }
  }

  return (
    <Box maxW="3xl" mx="auto" px={6} py={10}>
      <Heading size="lg" mb={2}>Profile</Heading>
      <Text opacity={0.8} mb={6}>
        Manage your account details. Sensitive changes require your current password.
      </Text>

      {(notice || error) && (
        <Box mb={6} borderWidth="1px" rounded="xl" p={4}>
          {notice && <Text>{notice}</Text>}
          {error && <Text>{error}</Text>}
        </Box>
      )}

      <Section title="Account info">
        <Row label="Username">{user.username}</Row>
        <Row label="Email">{user.email}</Row>
        <Row label="User ID">{String(user.id)}</Row>
      </Section>

      <Section title="Change username">
        <form onSubmit={submitUsername} noValidate>
          <Field label="New username">
            <Input
              value={shownUsername}
              onChange={(e) => setUsername(e.target.value)}
              placeholder={user.username}
            />
          </Field>
          <Button type="submit" width="100%" disabled={busy !== null}>
            {busy === "username" ? "Saving..." : "Update username"}
          </Button>
        </form>
      </Section>

      <Section title="Change email">
        <form onSubmit={submitEmail} noValidate>
          <Field label="New email">
            <Input
              value={shownEmail}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={user.email}
            />
          </Field>
          <Field label="Current password (required)">
            <Input
              type="password"
              value={emailPassword}
              onChange={(e) => setEmailPassword(e.target.value)}
              autoComplete="current-password"
              placeholder="••••••••"
            />
          </Field>
          <Button type="submit" width="100%" disabled={busy !== null}>
            {busy === "email" ? "Saving..." : "Update email"}
          </Button>
        </form>

        <Text mt={3} fontSize="sm" opacity={0.7}>
          Note: without email verification, changing email just changes your login identifier.
        </Text>
      </Section>

      <Section title="Change password">
        <form onSubmit={submitPassword} noValidate>
          <Field label="Current password">
            <Input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              autoComplete="current-password"
              placeholder="••••••••"
            />
          </Field>

          <Field label="New password">
            <Input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              autoComplete="new-password"
              placeholder="At least 8 characters"
            />
          </Field>

          <Button type="submit" width="100%" disabled={busy !== null}>
            {busy === "password" ? "Saving..." : "Update password"}
          </Button>
        </form>

        <Text mt={3} fontSize="sm" opacity={0.7}>
          After changing your password, you’ll be logged out.
        </Text>
      </Section>

      <Section title="Delete account" danger>
        <form onSubmit={submitDelete} noValidate>
          <Field label="Current password">
            <Input
              type="password"
              value={deletePassword}
              onChange={(e) => setDeletePassword(e.target.value)}
              autoComplete="current-password"
              placeholder="••••••••"
            />
          </Field>

          <Field label='Type "DELETE" to confirm'>
            <Input
              value={deleteConfirm}
              onChange={(e) => setDeleteConfirm(e.target.value)}
              placeholder="DELETE"
            />
          </Field>

          <Button type="submit" width="100%" disabled={busy !== null || !canDelete}>
            {busy === "delete" ? "Deleting..." : "Delete my account"}
          </Button>
        </form>

        <Text mt={3} fontSize="sm" opacity={0.7}>
          This permanently deletes your account and associated data.
        </Text>
      </Section>
    </Box>
  );
}

function Section({
  title,
  danger,
  children,
}: {
  title: string;
  danger?: boolean;
  children: React.ReactNode;
}) {
  return (
    <Box borderWidth="1px" rounded="xl" p={6} mb={6}>
      <Heading size="sm" mb={4} color={danger ? "red.300" : undefined}>
        {title}
      </Heading>
      {children}
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

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <Box display="flex" justifyContent="space-between" gap={4} mb={2}>
      <Text opacity={0.7}>{label}</Text>
      <Text fontFamily="mono">{children}</Text>
    </Box>
  );
}

type AxiosishError = {
  response?: { data?: unknown; status?: number };
  message?: string;
};

function extractErrorMessage(err: unknown, fallback: string): string {
  if (err instanceof Error) return err.message;

  const e = err as AxiosishError;
  const data = e?.response?.data;

  if (data && typeof data === "object" && "detail" in data) {
    const detail = (data as { detail: unknown }).detail;
    if (typeof detail === "string") return detail;
    return JSON.stringify(detail);
  }

  if (typeof data === "string") return data;
  if (typeof e?.message === "string") return e.message;

  return fallback;
}
