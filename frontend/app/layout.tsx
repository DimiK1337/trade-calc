import { Provider } from "@/components/ui/provider"
import { Box } from "@chakra-ui/react"

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
            <NavBar />
            {children}
          </Provider>
      </body>
    </html>
  )
}