import React from 'react';
import { clsx } from 'clsx';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  href?: string;
  external?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', children, href, external = false, className, ...props }, ref) => {
    const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

    const variantStyles = {
      primary: 'bg-medical-blue-600 text-white hover:bg-medical-blue-700 focus:ring-medical-blue-300 shadow-md hover:shadow-lg',
      secondary: 'bg-medical-green-600 text-white hover:bg-medical-green-700 focus:ring-medical-green-300 shadow-md hover:shadow-lg',
      outline: 'bg-transparent border-2 border-medical-blue-600 text-medical-blue-600 hover:bg-medical-blue-50 focus:ring-medical-blue-300',
      ghost: 'bg-transparent text-medical-blue-600 hover:bg-medical-blue-50 focus:ring-medical-blue-300',
    };

    const sizeStyles = {
      sm: 'px-4 py-2 text-sm',
      md: 'px-6 py-3 text-base',
      lg: 'px-8 py-4 text-lg',
    };

    const classes = clsx(baseStyles, variantStyles[variant], sizeStyles[size], className);

    if (href) {
      return (
        <a
          href={href}
          className={classes}
          target={external ? '_blank' : undefined}
          rel={external ? 'noopener noreferrer' : undefined}
        >
          {children}
        </a>
      );
    }

    return (
      <button ref={ref} className={classes} {...props}>
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
