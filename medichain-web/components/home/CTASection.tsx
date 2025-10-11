'use client';

import React from 'react';
import { ArrowRight, Book } from 'lucide-react';
import { Button, AnimatedSection } from '../shared';

export const CTASection: React.FC = () => {
  return (
    <section className="py-24 bg-gradient-to-r from-medical-blue-600 via-medical-blue-700 to-purple-700 relative overflow-hidden">
      {/* Decorative background */}
      <div className="absolute inset-0 bg-medical-pattern opacity-10" />

      <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <AnimatedSection animation="scale-in">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Experience MediChain?
          </h2>
          <p className="text-xl text-medical-blue-100 mb-10 max-w-3xl mx-auto">
            Test our multi-agent diagnostic system on Agentverse. Watch AI agents collaborate
            in real-time to provide transparent, evidence-based medical assessments.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button
              variant="primary"
              size="lg"
              href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
              external
              className="bg-white text-medical-blue-700 hover:bg-gray-50 shadow-2xl group"
            >
              Try Demo Now
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button
              variant="outline"
              size="lg"
              href="/docs"
              className="border-white text-white hover:bg-white/10"
            >
              <Book className="mr-2 w-5 h-5" />
              View Documentation
            </Button>
          </div>
        </AnimatedSection>
      </div>
    </section>
  );
};
