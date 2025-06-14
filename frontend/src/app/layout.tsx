import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains-mono',
});

export const metadata: Metadata = {
  title: 'Palmer AI - Product Intelligence Platform',
  description: 'Transform boring product descriptions into contractor gold with AI-powered intelligence. Built for HVAC, plumbing, and industrial distributors.',
  keywords: 'AI, B2B, product intelligence, distributors, HVAC, plumbing, contractors, Palmer AI',
  openGraph: {
    title: 'Palmer AI - Product Intelligence Platform',
    description: 'Transform boring product descriptions into contractor gold in minutes',
    url: 'https://palmer-apps.com',
    siteName: 'Palmer AI',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="font-sans antialiased bg-base text-textPrimary">
        {children}
      </body>
    </html>
  );
}
