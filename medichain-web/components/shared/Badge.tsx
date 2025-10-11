import React from 'react';
import { clsx } from 'clsx';

export interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  size = 'md',
  icon,
  className,
}) => {
  const baseStyles = 'inline-flex items-center gap-2 font-medium rounded-full';

  const variantStyles = {
    default: 'bg-gray-100 text-gray-700',
    primary: 'bg-medical-blue-100 text-medical-blue-700',
    success: 'bg-medical-green-100 text-medical-green-700',
    warning: 'bg-medical-amber-100 text-medical-amber-700',
    danger: 'bg-emergency-100 text-emergency-700',
    info: 'bg-blue-100 text-blue-700',
  };

  const sizeStyles = {
    sm: 'px-2.5 py-1 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  };

  return (
    <span className={clsx(baseStyles, variantStyles[variant], sizeStyles[size], className)}>
      {icon && <span className="flex-shrink-0">{icon}</span>}
      {children}
    </span>
  );
};
