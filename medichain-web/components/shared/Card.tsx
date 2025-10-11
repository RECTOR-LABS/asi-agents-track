import React from 'react';
import { clsx } from 'clsx';

export interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glassmorphism?: boolean;
  padding?: 'sm' | 'md' | 'lg';
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  hover = false,
  glassmorphism = false,
  padding = 'md',
}) => {
  const baseStyles = 'rounded-xl transition-all duration-300';

  const paddingStyles = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const styleVariant = glassmorphism
    ? 'backdrop-blur-lg bg-white/75 border border-gray-200/30 shadow-lg'
    : 'bg-white shadow-md border border-gray-100';

  const hoverStyles = hover ? 'hover:shadow-xl hover:-translate-y-1' : '';

  return (
    <div className={clsx(baseStyles, styleVariant, paddingStyles[padding], hoverStyles, className)}>
      {children}
    </div>
  );
};
