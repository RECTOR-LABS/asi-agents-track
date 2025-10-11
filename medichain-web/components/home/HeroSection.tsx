'use client';

import React from 'react';
import { Zap, ArrowRight } from 'lucide-react';
import { Button, Badge } from '../shared';

export const HeroSection: React.FC = () => {
  return (
    <section className="relative min-h-[90vh] flex items-center bg-gradient-to-br from-medical-blue-50 via-white to-medical-green-50 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-medical-pattern opacity-30" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        {/* Badge */}
        <div className="mb-6 animate-fade-in">
          <Badge variant="primary" size="md" icon={<Zap className="w-4 h-4" />}>
            Powered by ASI Alliance Technology
          </Badge>
        </div>

        {/* Main Headline */}
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight animate-slide-up">
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-medical-blue-600 to-medical-green-600">
            MediChain AI
          </span>
          <span className="block mt-3 text-gray-800">
            Decentralized Healthcare Diagnostics
          </span>
        </h1>

        {/* Subheadline */}
        <p className="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto mb-10 leading-relaxed">
          Multi-agent AI system leveraging <strong>Fetch.ai uAgents</strong> and{' '}
          <strong>SingularityNET MeTTa</strong> for transparent, evidence-based medical assessments.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
          <Button
            variant="primary"
            size="lg"
            href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
            external
            className="group"
          >
            Try Live Demo
            <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Button variant="outline" size="lg" href="/architecture">
            View Architecture
          </Button>
        </div>

        {/* Innovation Lab Badges */}
        <div className="flex flex-wrap gap-3 justify-center items-center">
          <img
            src="https://img.shields.io/badge/innovationlab-3D8BD3?style=for-the-badge"
            alt="Innovation Lab"
            className="h-8"
          />
          <img
            src="https://img.shields.io/badge/hackathon-5F43F1?style=for-the-badge"
            alt="Hackathon"
            className="h-8"
          />
          <img
            src="https://img.shields.io/badge/ASI_Alliance-10B981?style=for-the-badge"
            alt="ASI Alliance"
            className="h-8"
          />
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-medical-blue-300 rounded-full flex justify-center">
            <div className="w-1 h-3 bg-medical-blue-500 rounded-full mt-2 animate-pulse" />
          </div>
        </div>
      </div>
    </section>
  );
};
