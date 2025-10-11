'use client';

import React from 'react';
import { clsx } from 'clsx';

export interface StatusIndicatorProps {
  status: 'active' | 'inactive' | 'checking' | 'error';
  label?: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  pulse?: boolean;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  label,
  size = 'md',
  showLabel = true,
  pulse = true,
}) => {
  const dotSizeStyles = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };

  const textSizeStyles = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  };

  const statusConfig = {
    active: {
      color: 'bg-medical-green-500',
      label: label || 'Active',
      textColor: 'text-medical-green-700',
    },
    inactive: {
      color: 'bg-gray-400',
      label: label || 'Inactive',
      textColor: 'text-gray-600',
    },
    checking: {
      color: 'bg-medical-amber-500',
      label: label || 'Checking...',
      textColor: 'text-medical-amber-700',
    },
    error: {
      color: 'bg-emergency-500',
      label: label || 'Error',
      textColor: 'text-emergency-700',
    },
  };

  const config = statusConfig[status];
  const shouldPulse = pulse && (status === 'active' || status === 'checking');

  return (
    <div className="inline-flex items-center gap-2">
      <div className="relative">
        <div className={clsx('rounded-full', dotSizeStyles[size], config.color)} />
        {shouldPulse && (
          <div
            className={clsx(
              'absolute inset-0 rounded-full animate-pulse-slow',
              dotSizeStyles[size],
              config.color,
              'opacity-75'
            )}
          />
        )}
      </div>
      {showLabel && (
        <span className={clsx('font-medium', textSizeStyles[size], config.textColor)}>
          {config.label}
        </span>
      )}
    </div>
  );
};
