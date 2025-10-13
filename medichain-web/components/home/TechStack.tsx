'use client';

import React from 'react';
import { AnimatedSection, Card } from '../shared';

const technologies = [
  { name: 'Fetch.ai uAgents', category: 'Multi-Agent Framework', color: 'border-l-medical-blue-500' },
  { name: 'SingularityNET MeTTa', category: 'Knowledge Graph Engine', color: 'border-l-purple-500' },
  { name: 'Agentverse', category: 'Agent Deployment Platform', color: 'border-l-medical-green-500' },
  { name: 'Next.js 14', category: 'Web Framework', color: 'border-l-gray-700' },
  { name: 'TypeScript', category: 'Type-Safe Development', color: 'border-l-blue-500' },
  { name: 'Tailwind CSS', category: 'Styling Framework', color: 'border-l-cyan-500' },
];

export const TechStack: React.FC = () => {
  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-medical-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <AnimatedSection animation="slide-up" className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Built with Excellence
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Leveraging industry-leading technologies for production-grade healthcare AI.
          </p>
        </AnimatedSection>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {technologies.map((tech, index) => (
            <AnimatedSection key={index} animation="scale-in" delay={index * 75}>
              <Card
                hover
                className={`border-l-4 ${tech.color} transition-all duration-300 hover:scale-105 hover:shadow-xl`}
              >
                <h3 className="text-lg font-bold text-gray-900 mb-1">{tech.name}</h3>
                <p className="text-sm text-gray-600">{tech.category}</p>
              </Card>
            </AnimatedSection>
          ))}
        </div>

        <AnimatedSection animation="slide-up" delay={400} className="mt-16 text-center">
          <Card glassmorphism padding="lg" className="max-w-4xl mx-auto">
            <p className="text-gray-700 leading-relaxed mb-4">
              <strong>Production-Ready Architecture:</strong> VPS-hosted agents with systemd services,
              Vercel-deployed frontend, 24/7 uptime monitoring, and Chat Protocol integration for
              ASI:One compatibility.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
              <div className="text-center">
                <p className="text-2xl font-bold text-medical-blue-600">25</p>
                <p className="text-sm text-gray-600">Conditions</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-purple-600">2,074</p>
                <p className="text-sm text-gray-600">Medical Facts</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-medical-green-600">180</p>
                <p className="text-sm text-gray-600">Risk Factors</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-orange-600">181</p>
                <p className="text-sm text-gray-600">Tests Passing</p>
              </div>
            </div>
          </Card>
        </AnimatedSection>
      </div>
    </section>
  );
};
