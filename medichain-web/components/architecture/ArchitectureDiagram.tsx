'use client';

import React from 'react';

export const ArchitectureDiagram: React.FC = () => {
  return (
    <svg
      viewBox="0 0 800 700"
      className="w-full h-auto"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <marker
          id="arrowhead"
          markerWidth="10"
          markerHeight="10"
          refX="9"
          refY="3"
          orient="auto"
        >
          <polygon points="0 0, 10 3, 0 6" fill="#3B82F6" />
        </marker>

        <linearGradient id="blueGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.1" />
          <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.05" />
        </linearGradient>

        <linearGradient id="purpleGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#9333EA" stopOpacity="0.1" />
          <stop offset="100%" stopColor="#9333EA" stopOpacity="0.05" />
        </linearGradient>

        <linearGradient id="greenGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#10B981" stopOpacity="0.1" />
          <stop offset="100%" stopColor="#10B981" stopOpacity="0.05" />
        </linearGradient>

        <linearGradient id="amberGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#F59E0B" stopOpacity="0.1" />
          <stop offset="100%" stopColor="#F59E0B" stopOpacity="0.05" />
        </linearGradient>
      </defs>

      {/* USER Box */}
      <g>
        <rect x="200" y="20" width="400" height="80" rx="8" fill="url(#blueGradient)" stroke="#3B82F6" strokeWidth="2"/>
        <text x="400" y="50" textAnchor="middle" fontSize="16" fontWeight="600" fill="#1F2937">USER (Agentverse Chat)</text>
        <text x="400" y="75" textAnchor="middle" fontSize="12" fill="#6B7280">↓ Chat Protocol ↑</text>
      </g>

      {/* Arrow from USER to COORDINATOR */}
      <line x1="400" y1="100" x2="400" y2="150" stroke="#3B82F6" strokeWidth="2" markerEnd="url(#arrowhead)"/>

      {/* COORDINATOR Box */}
      <g>
        <rect x="280" y="150" width="240" height="100" rx="8" fill="url(#blueGradient)" stroke="#3B82F6" strokeWidth="2"/>
        <text x="400" y="180" textAnchor="middle" fontSize="16" fontWeight="bold" fill="#1F2937">COORDINATOR</text>
        <text x="400" y="200" textAnchor="middle" fontSize="12" fill="#6B7280">(Port 8001)</text>
        <text x="400" y="220" textAnchor="middle" fontSize="12" fill="#6B7280">• Session Mgmt</text>
        <text x="400" y="235" textAnchor="middle" fontSize="12" fill="#6B7280">• Agent Routing</text>
      </g>

      {/* Arrows from COORDINATOR to 3 agents */}
      <line x1="320" y1="250" x2="140" y2="330" stroke="#3B82F6" strokeWidth="2" markerEnd="url(#arrowhead)"/>
      <line x1="400" y1="250" x2="400" y2="330" stroke="#3B82F6" strokeWidth="2" markerEnd="url(#arrowhead)"/>
      <line x1="480" y1="250" x2="660" y2="330" stroke="#3B82F6" strokeWidth="2" markerEnd="url(#arrowhead)"/>

      {/* INTAKE Agent */}
      <g>
        <rect x="40" y="330" width="200" height="120" rx="8" fill="url(#purpleGradient)" stroke="#9333EA" strokeWidth="2"/>
        <text x="140" y="360" textAnchor="middle" fontSize="16" fontWeight="bold" fill="#1F2937">INTAKE</text>
        <text x="140" y="380" textAnchor="middle" fontSize="12" fill="#6B7280">(Port 8000)</text>
        <line x1="50" y1="390" x2="230" y2="390" stroke="#E5E7EB" strokeWidth="1"/>
        <text x="140" y="410" textAnchor="middle" fontSize="12" fill="#6B7280">• NLP Extract</text>
        <text x="140" y="430" textAnchor="middle" fontSize="12" fill="#6B7280">• Demographics</text>
      </g>

      {/* SYMPTOM Agent */}
      <g>
        <rect x="300" y="330" width="200" height="120" rx="8" fill="url(#greenGradient)" stroke="#10B981" strokeWidth="2"/>
        <text x="400" y="360" textAnchor="middle" fontSize="16" fontWeight="bold" fill="#1F2937">SYMPTOM</text>
        <text x="400" y="380" textAnchor="middle" fontSize="12" fill="#6B7280">(8004)</text>
        <line x1="310" y1="390" x2="490" y2="390" stroke="#E5E7EB" strokeWidth="1"/>
        <text x="400" y="410" textAnchor="middle" fontSize="12" fill="#6B7280">• Triage</text>
        <text x="400" y="430" textAnchor="middle" fontSize="12" fill="#6B7280">• Flags</text>
      </g>

      {/* TREATMENT Agent */}
      <g>
        <rect x="560" y="330" width="200" height="120" rx="8" fill="url(#amberGradient)" stroke="#F59E0B" strokeWidth="2"/>
        <text x="660" y="360" textAnchor="middle" fontSize="16" fontWeight="bold" fill="#1F2937">TREATMENT</text>
        <text x="660" y="380" textAnchor="middle" fontSize="12" fill="#6B7280">(Port 8005)</text>
        <line x1="570" y1="390" x2="750" y2="390" stroke="#E5E7EB" strokeWidth="1"/>
        <text x="660" y="410" textAnchor="middle" fontSize="12" fill="#6B7280">• Safety Check</text>
        <text x="660" y="430" textAnchor="middle" fontSize="12" fill="#6B7280">• Drug Interact</text>
      </g>

      {/* Arrows from 3 agents to MeTTa KB */}
      <line x1="140" y1="450" x2="340" y2="540" stroke="#3B82F6" strokeWidth="2" markerEnd="url(#arrowhead)"/>
      <line x1="400" y1="450" x2="400" y2="540" stroke="#3B82F6" strokeWidth="2" markerEnd="url(#arrowhead)"/>
      <line x1="660" y1="450" x2="460" y2="540" stroke="#3B82F6" strokeWidth="2" markerEnd="url(#arrowhead)"/>

      {/* MeTTa KB Box */}
      <g>
        <rect x="280" y="540" width="240" height="120" rx="8" fill="url(#purpleGradient)" stroke="#9333EA" strokeWidth="2"/>
        <text x="400" y="570" textAnchor="middle" fontSize="16" fontWeight="bold" fill="#1F2937">METTA KB</text>
        <line x1="290" y1="580" x2="510" y2="580" stroke="#E5E7EB" strokeWidth="1"/>
        <text x="400" y="605" textAnchor="middle" fontSize="12" fill="#6B7280">• 13 Conditions</text>
        <text x="400" y="625" textAnchor="middle" fontSize="12" fill="#6B7280">• 200+ Facts</text>
        <text x="400" y="645" textAnchor="middle" fontSize="12" fill="#6B7280">• 45+ Contraind.</text>
      </g>
    </svg>
  );
};
