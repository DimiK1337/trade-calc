"use client";

import NextLink from "next/link";
import { Box, Flex, Text } from "@chakra-ui/react";
import { usePathname } from "next/navigation";

import { useAuth } from "@/app/auth/AuthProvider";
import { colorFromString, initialsFromUser } from "@/lib/auth";

interface NavItem {
  href: string;
  label: string;
}

const NAV: NavItem[] = [
  { href: "/calculator", label: "Calculator" },
  { href: "/trade-planner", label: "Trade Planner" },
];

export default function NavBar() {
  const pathname = usePathname();
  const { user, isLoading, logout } = useAuth();

  return (
    <Box borderBottomWidth="1px">
      <Flex
        maxW="5xl"
        mx="auto"
        px={6}
        py={4}
        align="center"
        justify="space-between"
        gap={6}
      >
        <NextLink href="/calculator" style={{ textDecoration: "none" }}>
          <Text fontWeight="bold">Trade Calc</Text>
        </NextLink>

        <Flex gap={2} wrap="wrap" align="center">
          {NAV.map((item) => {
            const active =
              pathname === item.href || pathname.startsWith(item.href + "/");

            return (
              <NextLink
                key={item.href}
                href={item.href}
                style={{ textDecoration: "none" }}
              >
                <Box
                  px={3}
                  py={2}
                  rounded="md"
                  borderWidth="1px"
                  opacity={active ? 1 : 0.75}
                  fontWeight={active ? "semibold" : "normal"}
                >
                  {item.label}
                </Box>
              </NextLink>
            );
          })}

          <Box w="1px" h="28px" bg="currentColor" opacity={0.15} mx={2} />

          {isLoading ? (
            <Text fontSize="sm" opacity={0.7}>
              …
            </Text>
          ) : user ? (
            <Flex align="center" gap={2}>
              <UserPill email={user.email} username={user.username} />
              <Box
                as="button"
                onClick={logout}
                px={3}
                py={2}
                rounded="md"
                borderWidth="1px"
                opacity={0.85}
              >
                Logout
              </Box>
            </Flex>
          ) : (
            <Flex gap={2}>
              <NextLink href="/login" style={{ textDecoration: "none" }}>
                <Box px={3} py={2} rounded="md" borderWidth="1px">
                  Login
                </Box>
              </NextLink>

              <NextLink href="/register" style={{ textDecoration: "none" }}>
                <Box px={3} py={2} rounded="md" borderWidth="1px" fontWeight="semibold">
                  Register
                </Box>
              </NextLink>
            </Flex>
          )}
        </Flex>
      </Flex>
    </Box>
  );
}

function UserPill({ email, username }: { email: string; username: string }) {
  const initials = initialsFromUser({ email, username });
  const bg = colorFromString(email || username);

  return (
    <Flex align="center" gap={2} borderWidth="1px" rounded="full" px={3} py={1.5}>
      <Box
        width="28px"
        height="28px"
        rounded="full"
        display="flex"
        alignItems="center"
        justifyContent="center"
        color="white"
        style={{ background: bg }}
        fontSize="xs"
        fontWeight="bold"
      >
        {initials}
      </Box>

      <Box>
        <Text fontSize="sm" lineHeight="1" fontWeight="semibold">
          {username}
        </Text>
        <Text fontSize="xs" opacity={0.7} lineHeight="1.1">
          {email}
        </Text>
      </Box>
    </Flex>
  );
}
