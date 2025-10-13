'use client';

import React, { useState } from 'react';
import { Check, Copy, Sparkles } from 'lucide-react';
import { clsx } from 'clsx';

export interface CodeBlockProps {
  code: string;
  language: string;
  title?: string;
  showLineNumbers?: boolean;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language,
  title,
  showLineNumbers = false,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getLineColor = (line: string, lang: string): string => {
    // Dark theme colors for code block
    if (lang === 'python') {
      if (line.trim().startsWith('#')) return 'text-gray-500 italic';
      if (line.includes('"""') || line.includes("'''")) return 'text-emerald-400 italic';
      if (line.includes('def ') || line.includes('class ')) return 'text-purple-400 font-semibold';
      if (line.includes('import ') || line.includes('from ')) return 'text-pink-400';
      if (line.includes('return ') || line.includes('async ') || line.includes('await ')) return 'text-cyan-400';
      if (line.includes('@')) return 'text-yellow-400'; // Decorators
      if (line.includes('None') || line.includes('True') || line.includes('False')) return 'text-orange-400';
    } else if (lang === 'bash') {
      if (line.trim().startsWith('#')) return 'text-gray-500 italic';
      if (line.trim().startsWith('sudo ')) return 'text-red-400 font-semibold';
      if (line.includes('systemctl') || line.includes('journalctl')) return 'text-cyan-400';
      if (line.includes('python ') || line.includes('pytest ')) return 'text-yellow-400';
      if (line.includes('apt ') || line.includes('pip ')) return 'text-green-400';
    } else if (lang === 'metta') {
      if (line.trim().startsWith(';')) return 'text-gray-500 italic';
      if (line.includes('(has-') || line.includes('(requires-')) return 'text-pink-400';
      if (line.includes('(red-flag-') || line.includes('(contraindication')) return 'text-red-400';
    }
    return 'text-gray-200';
  };

  const renderLines = (code: string, lang: string) => {
    const lines = code.split('\n');

    return lines.map((line, index) => {
      const colorClass = getLineColor(line, lang);

      return (
        <div key={index} className="flex hover:bg-white/5 transition-colors group/line">
          {showLineNumbers && (
            <span className="text-gray-600 select-none w-12 inline-block text-right pr-4 flex-shrink-0">
              {index + 1}
            </span>
          )}
          <span className={`flex-1 ${colorClass}`}>
            {line || ' '}
          </span>
        </div>
      );
    });
  };

  const getLanguageColor = (lang: string) => {
    const colors: Record<string, string> = {
      python: 'bg-blue-500',
      bash: 'bg-green-500',
      metta: 'bg-pink-500',
      typescript: 'bg-blue-600',
      javascript: 'bg-yellow-500',
    };
    return colors[lang] ?? 'bg-gray-500';
  };

  return (
    <div className="group relative">
      {/* Gradient border effect */}
      <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl opacity-20 group-hover:opacity-40 blur transition-all duration-500"></div>

      <div className="relative bg-gradient-to-br from-gray-900 via-gray-900 to-gray-800 rounded-2xl overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 bg-gray-800/50 backdrop-blur border-b border-gray-700/50">
          <div className="flex items-center gap-3">
            {/* Window buttons */}
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
            </div>

            {title && (
              <span className="text-gray-300 text-sm font-medium ml-2">{title}</span>
            )}
          </div>

          <div className="flex items-center gap-3">
            {/* Language badge */}
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-gray-700/50 border border-gray-600/50">
              <div className={clsx('w-2 h-2 rounded-full', getLanguageColor(language))}></div>
              <span className="text-xs text-gray-300 font-medium uppercase tracking-wider">
                {language}
              </span>
            </div>

            {/* Copy button */}
            <button
              onClick={handleCopy}
              aria-label={copied ? "Code copied to clipboard" : "Copy code to clipboard"}
              className={clsx(
                'flex items-center gap-2 px-3 py-1.5 rounded-lg font-medium text-sm transition-all',
                copied
                  ? 'bg-green-500/20 text-green-400 border border-green-500/50'
                  : 'bg-gray-700/50 text-gray-300 border border-gray-600/50 hover:bg-gray-600/50 hover:border-gray-500/50'
              )}
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4" />
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Code content */}
        <div className="overflow-x-auto">
          <div className="p-6 font-mono text-sm leading-relaxed">
            {renderLines(code, language)}
          </div>
        </div>

        {/* Sparkle decoration */}
        <Sparkles className="absolute top-4 right-4 w-4 h-4 text-purple-400/20 group-hover:text-purple-400/40 transition-colors" />
      </div>
    </div>
  );
};
