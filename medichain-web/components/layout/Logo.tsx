import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

export interface LogoProps {
  variant?: 'horizontal' | 'icon' | 'vertical';
  size?: 'sm' | 'md' | 'lg';
  href?: string;
}

export const Logo: React.FC<LogoProps> = ({ variant = 'horizontal', size = 'md', href = '/' }) => {
  const sizeConfig = {
    horizontal: {
      sm: { width: 150, height: 40 },
      md: { width: 200, height: 50 },
      lg: { width: 250, height: 65 },
    },
    icon: {
      sm: { width: 32, height: 32 },
      md: { width: 40, height: 40 },
      lg: { width: 48, height: 48 },
    },
    vertical: {
      sm: { width: 80, height: 100 },
      md: { width: 100, height: 120 },
      lg: { width: 120, height: 150 },
    },
  };

  const logoPath = variant === 'icon' ? '/logo-icon.svg' : variant === 'vertical' ? '/logo-vertical.svg' : '/logo.svg';
  const dimensions = sizeConfig[variant][size];

  return (
    <Link href={href} className="inline-block">
      <Image
        src={logoPath}
        alt="MediChain AI Logo"
        width={dimensions.width}
        height={dimensions.height}
        priority
        className="transition-opacity hover:opacity-80"
      />
    </Link>
  );
};
