import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Github, Globe } from 'lucide-react';
import { Logo } from './Logo';

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Column */}
          <div className="col-span-1 md:col-span-2">
            <div className="mb-4 brightness-0 invert">
              <Logo variant="horizontal" size="md" />
            </div>
            <p className="text-gray-400 text-sm max-w-md mb-4">
              Decentralized healthcare diagnostics powered by ASI Alliance technology.
              Built with Fetch.ai uAgents and SingularityNET MeTTa.
            </p>
            <div className="flex gap-4">
              <a
                href="https://github.com/RECTOR-LABS/asi-agents-track"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="GitHub"
              >
                <Github size={20} />
              </a>
              <a
                href="https://fetch.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="Fetch.ai"
              >
                <Globe size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/" className="text-gray-400 hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-400 hover:text-white transition-colors">
                  About
                </Link>
              </li>
              <li>
                <Link href="/architecture" className="text-gray-400 hover:text-white transition-colors">
                  Architecture
                </Link>
              </li>
              <li>
                <Link href="/demo" className="text-gray-400 hover:text-white transition-colors">
                  Demo
                </Link>
              </li>
              <li>
                <Link href="/docs" className="text-gray-400 hover:text-white transition-colors">
                  Documentation
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a
                  href="https://fetch.ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Fetch.ai
                </a>
              </li>
              <li>
                <a
                  href="https://singularitynet.io"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  SingularityNET
                </a>
              </li>
              <li>
                <a
                  href="https://agentverse.ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Agentverse
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/RECTOR-LABS/asi-agents-track"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  GitHub Repository
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-center md:text-left">
              <p className="text-sm text-gray-400">
                ASI Agents Track Hackathon {currentYear} | Built for transparent AI healthcare
              </p>
              <p className="text-xs text-gray-500 mt-1">
                <strong>Medical Disclaimer:</strong> This is an AI diagnostic tool for educational purposes only.
                Not a substitute for professional medical advice.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Image
                src="https://img.shields.io/badge/innovationlab-3D8BD3?style=flat-square"
                alt="Innovation Lab"
                width={110}
                height={20}
                className="h-5"
                unoptimized
              />
              <Image
                src="https://img.shields.io/badge/hackathon-5F43F1?style=flat-square"
                alt="Hackathon"
                width={90}
                height={20}
                className="h-5"
                unoptimized
              />
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};
