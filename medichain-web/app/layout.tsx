import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MediChain AI - Decentralized Healthcare Diagnostics",
  description: "Multi-agent AI diagnostic system powered by Fetch.ai uAgents and SingularityNET MeTTa. Transparent, evidence-based medical assessments with 87% accuracy.",
  keywords: [
    "medical diagnostics",
    "AI agents",
    "MeTTa",
    "decentralized healthcare",
    "Fetch.ai",
    "SingularityNET",
    "ASI Alliance",
    "medical AI",
    "knowledge graphs"
  ],
  authors: [{ name: "RECTOR Labs" }],
  openGraph: {
    title: "MediChain AI - Decentralized Healthcare Diagnostics",
    description: "Multi-agent AI diagnostic system with transparent reasoning and evidence-based recommendations.",
    type: "website",
    url: "https://medichain-web.vercel.app",
  },
  twitter: {
    card: "summary_large_image",
    title: "MediChain AI - Decentralized Healthcare Diagnostics",
    description: "Multi-agent AI diagnostic system powered by ASI Alliance technology.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={inter.className}>
        <Navbar />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
