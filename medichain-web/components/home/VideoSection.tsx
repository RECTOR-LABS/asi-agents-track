'use client';

import React from 'react';
import { Play } from 'lucide-react';
import { AnimatedSection, Card } from '../shared';

export const VideoSection: React.FC = () => {
  return (
    <section className="relative py-24 bg-gradient-to-br from-medical-blue-900 via-purple-900 to-gray-900 overflow-hidden">
      {/* Animated Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-96 h-96 bg-medical-blue-500/20 rounded-full blur-3xl -top-20 -left-20 animate-pulse" />
        <div className="absolute w-96 h-96 bg-purple-500/20 rounded-full blur-3xl -bottom-20 -right-20 animate-pulse delay-1000" />
        <div className="absolute w-96 h-96 bg-medical-green-500/10 rounded-full blur-3xl top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-pulse delay-500" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <AnimatedSection animation="fade-in" className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full text-white mb-6 border border-white/20">
            <Play className="w-5 h-5 text-medical-green-400" />
            <span className="font-semibold">Watch Demo</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            See MediChain AI in Action
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Experience the power of multi-agent AI diagnostics with transparent reasoning and evidence-based recommendations
          </p>
        </AnimatedSection>

        {/* Video Container with Stunning Effects */}
        <AnimatedSection animation="scale-in" delay={200}>
          <div className="relative max-w-5xl mx-auto">
            {/* Glow Effect Background */}
            <div className="absolute inset-0 bg-gradient-to-r from-medical-blue-500 via-purple-500 to-medical-green-500 rounded-3xl blur-2xl opacity-30 animate-pulse" />

            {/* Video Card with Glass Morphism */}
            <Card
              className="relative overflow-hidden rounded-3xl border-2 border-white/20 shadow-2xl backdrop-blur-sm bg-white/5 p-0"
            >
              {/* Video Wrapper with 16:9 Aspect Ratio */}
              <div className="relative" style={{ paddingBottom: '56.25%' }}>
                <iframe
                  className="absolute top-0 left-0 w-full h-full rounded-3xl"
                  src="https://www.youtube.com/embed/Fjz9C6GShIQ?rel=0&modestbranding=1&autohide=1&showinfo=0"
                  title="MediChain AI Demo Video"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>

              {/* Decorative Corner Accents */}
              <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-medical-blue-500/20 to-transparent rounded-tl-3xl" />
              <div className="absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-tl from-medical-green-500/20 to-transparent rounded-br-3xl" />
            </Card>

            {/* Floating Elements for Visual Interest */}
            <div className="absolute -top-8 -right-8 w-16 h-16 bg-medical-green-500/30 rounded-full blur-xl animate-bounce delay-200" />
            <div className="absolute -bottom-8 -left-8 w-20 h-20 bg-purple-500/30 rounded-full blur-xl animate-bounce delay-500" />
          </div>
        </AnimatedSection>

        {/* Video Stats/Highlights */}
        <AnimatedSection animation="slide-up" delay={400} className="mt-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {[
              { label: 'Multi-Agent Flow', value: '4 Agents', icon: '🤖' },
              { label: 'Response Time', value: '~15 sec', icon: '⚡' },
              { label: 'Medical Conditions', value: '25 Total', icon: '🏥' },
              { label: 'Test Accuracy', value: '87%', icon: '✅' },
            ].map((stat, index) => (
              <div
                key={index}
                className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/10 hover:bg-white/15 transition-all hover:scale-105"
              >
                <div className="text-3xl mb-2">{stat.icon}</div>
                <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-sm text-gray-300">{stat.label}</div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Call to Action */}
        <AnimatedSection animation="fade-in" delay={600} className="text-center mt-12">
          <p className="text-gray-300 mb-6">
            Ready to test the system yourself?
          </p>
          <a
            href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-medical-blue-600 to-medical-green-600 text-white rounded-xl font-bold text-lg hover:scale-105 transition-transform shadow-2xl hover:shadow-medical-blue-500/50"
          >
            <Play className="w-6 h-6" />
            Try Live Demo on Agentverse
          </a>
        </AnimatedSection>
      </div>

      {/* Additional Decorative Elements */}
      <style jsx>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 0.3;
          }
          50% {
            opacity: 0.5;
          }
        }

        .delay-200 {
          animation-delay: 200ms;
        }

        .delay-500 {
          animation-delay: 500ms;
        }

        .delay-1000 {
          animation-delay: 1000ms;
        }
      `}</style>
    </section>
  );
};
