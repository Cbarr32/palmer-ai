import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Palmer AI - B2B Product Intelligence Platform',
  description: 'AI-powered product descriptions for industrial distributors. Transform your catalog with Claude Sonnet 4.',
  keywords: 'B2B, product intelligence, AI, distributors, industrial equipment',
  authors: [{ name: 'Palmer AI' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#8b5cf6',
  openGraph: {
    title: 'Palmer AI - B2B Product Intelligence',
    description: 'Transform your product catalog with AI',
    url: 'https://palmerai.com',
    siteName: 'Palmer AI',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
