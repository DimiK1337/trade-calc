"use client";

import NextLink from "next/link";
import { Box, Flex, Text } from "@chakra-ui/react";
import { usePathname } from "next/navigation";

interface NavItem {
  href: string;
  label: string;
}

const NAV: NavItem[] = [
  { href: "/calculator", label: "Calculator" },
  { href: "/trade-planner", label: "Trade Planner" },
  // Later:
  // { href: "/journal", label: "Journal" },
  // { href: "/analytics", label: "Analytics" },
  // { href: "/accounts", label: "Accounts" },
];

export default function NavBar() {
  const pathname = usePathname();

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
        <Text fontWeight="bold">Trade Calc</Text>

        <Flex gap={2} wrap="wrap">
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
        </Flex>
      </Flex>
    </Box>
  );
}
