'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';
import { Logo } from './Logo';
import { Button } from '../shared';
import { clsx } from 'clsx';

const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/architecture', label: 'Architecture' },
  { href: '/demo', label: 'Demo' },
  { href: '/docs', label: 'Docs' },
];

export const Navbar: React.FC = () => {
  const pathname = usePathname();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      className={clsx(
        'sticky top-0 z-50 transition-all duration-300',
        isScrolled
          ? 'backdrop-blur-lg bg-white/90 border-b border-gray-200 shadow-sm'
          : 'bg-transparent'
      )}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Logo variant="horizontal" size="md" />

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={clsx(
                  'text-sm font-medium transition-colors duration-200 drop-shadow-sm',
                  pathname === link.href
                    ? 'text-medical-blue-600'
                    : isScrolled ? 'text-gray-600 hover:text-medical-blue-600' : 'text-gray-900 hover:text-medical-blue-600'
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* CTA Button - Desktop */}
          <div className="hidden md:block">
            <Button
              variant="primary"
              size="sm"
              href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
              external
            >
              Try Demo
            </Button>
          </div>

          {/* Mobile Menu Toggle */}
          <button
            className="md:hidden p-2 text-gray-600 hover:text-medical-blue-600 transition-colors"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200 animate-slide-down">
            <div className="flex flex-col gap-3">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={clsx(
                    'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                    pathname === link.href
                      ? 'bg-medical-blue-50 text-medical-blue-600'
                      : 'text-gray-600 hover:bg-gray-50'
                  )}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
              <div className="px-4 pt-2">
                <Button
                  variant="primary"
                  size="sm"
                  href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
                  external
                  className="w-full"
                >
                  Try Demo
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};
