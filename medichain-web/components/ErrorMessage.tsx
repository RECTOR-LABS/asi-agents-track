'use client';

import { AlertCircle, XCircle } from 'lucide-react';
import clsx from 'clsx';

interface ErrorMessageProps {
  title?: string;
  message: string;
  type?: 'error' | 'warning';
  className?: string;
}

export default function ErrorMessage({
  title,
  message,
  type = 'error',
  className,
}: ErrorMessageProps) {
  const isError = type === 'error';

  return (
    <div
      className={clsx(
        'rounded-lg border p-4',
        isError
          ? 'bg-emergency-50 border-emergency-200'
          : 'bg-urgent-50 border-urgent-200',
        className
      )}
      role="alert"
    >
      <div className="flex items-start gap-3">
        {isError ? (
          <XCircle className="w-5 h-5 text-emergency-600 flex-shrink-0 mt-0.5" />
        ) : (
          <AlertCircle className="w-5 h-5 text-urgent-600 flex-shrink-0 mt-0.5" />
        )}
        <div className="flex-1">
          {title && (
            <h3
              className={clsx(
                'text-sm font-semibold mb-1',
                isError ? 'text-emergency-900' : 'text-urgent-900'
              )}
            >
              {title}
            </h3>
          )}
          <p
            className={clsx(
              'text-sm',
              isError ? 'text-emergency-700' : 'text-urgent-700'
            )}
          >
            {message}
          </p>
        </div>
      </div>
    </div>
  );
}
