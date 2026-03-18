import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'StatChicane',
  description: 'F1 Intelligence Platform — Ask questions, analyse telemetry.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-text-primary font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
