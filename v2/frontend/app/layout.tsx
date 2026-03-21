import type { Metadata } from 'next'
import './globals.css'
import AppShell from '@/components/layout/AppShell'

export const metadata: Metadata = {
  title: 'StatChicane',
  description: 'F1 Intelligence Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-text-primary font-sans
                       antialiased overflow-hidden">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  )
}
