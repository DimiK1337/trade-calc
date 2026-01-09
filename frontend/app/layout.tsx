import { Provider } from "@/components/ui/provider";
import { AuthProvider } from "@/app/auth/AuthProvider";

import NavBar from "@/components/NavBar"
interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout(props: RootLayoutProps) {
  const { children } = props
  return (
    <html suppressHydrationWarning lang="en">
      <body>
        <Provider>
          <AuthProvider>
            <NavBar />
            {children}
          </AuthProvider>
        </Provider>
      </body>
    </html>
  )
}