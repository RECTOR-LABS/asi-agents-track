'use client';

import React, { useEffect, useRef, useState } from 'react';
import { clsx } from 'clsx';

export interface AnimatedSectionProps {
  children: React.ReactNode;
  animation?: 'fade-in' | 'slide-up' | 'slide-down' | 'scale-in';
  delay?: number;
  threshold?: number;
  className?: string;
}

export const AnimatedSection: React.FC<AnimatedSectionProps> = ({
  children,
  animation = 'fade-in',
  delay = 0,
  threshold = 0.1,
  className,
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry && entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      observer.disconnect();
    };
  }, [threshold]);

  const animationStyles = {
    'fade-in': isVisible ? 'opacity-100' : 'opacity-0',
    'slide-up': isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0',
    'slide-down': isVisible ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0',
    'scale-in': isVisible ? 'scale-100 opacity-100' : 'scale-95 opacity-0',
  };

  return (
    <div
      ref={ref}
      className={clsx('transform transition-all duration-700', animationStyles[animation], className)}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
};
