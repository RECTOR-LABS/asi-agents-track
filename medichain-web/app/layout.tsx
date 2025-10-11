import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MediChain AI - Decentralized Medical Diagnostics",
  description: "AI-powered medical diagnostic system leveraging multi-agent architecture and MeTTa knowledge graphs for evidence-based health assessments.",
  keywords: ["medical diagnostics", "AI agents", "MeTTa", "decentralized", "healthcare"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
