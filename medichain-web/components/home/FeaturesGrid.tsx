'use client';

import React from 'react';
import { Search, GitBranch, Shield, Zap, Clock, Globe } from 'lucide-react';
import { Card, AnimatedSection } from '../shared';

const features = [
  {
    icon: <Search className="w-6 h-6" />,
    title: 'Transparent Reasoning',
    description: 'See how AI makes decisions with complete reasoning chains, differential diagnoses, and confidence scores.',
    color: 'text-medical-blue-600',
    bgColor: 'bg-medical-blue-100',
  },
  {
    icon: <GitBranch className="w-6 h-6" />,
    title: 'Decentralized Multi-Agent',
    description: '4 specialized agents collaborate: Coordinator, Patient Intake, Symptom Analysis, and Treatment Recommendation.',
    color: 'text-purple-600',
    bgColor: 'bg-purple-100',
  },
  {
    icon: <Zap className="w-6 h-6" />,
    title: 'Fast Diagnosis',
    description: 'Comprehensive diagnostic results in ~15 seconds through efficient multi-agent communication.',
    color: 'text-medical-green-600',
    bgColor: 'bg-medical-green-100',
  },
  {
    icon: <Shield className="w-6 h-6" />,
    title: 'Evidence-Based',
    description: '200+ medical facts from CDC, WHO, AHA, Johns Hopkins with 45+ contraindication checks.',
    color: 'text-blue-600',
    bgColor: 'bg-blue-100',
  },
  {
    icon: <Clock className="w-6 h-6" />,
    title: 'Privacy-First',
    description: 'No patient data stored. All processing happens in real-time with mailbox communication.',
    color: 'text-gray-600',
    bgColor: 'bg-gray-100',
  },
  {
    icon: <Globe className="w-6 h-6" />,
    title: '24/7 Accessible',
    description: 'Available anywhere, anytime via Agentverse platform with 99.9% uptime on VPS infrastructure.',
    color: 'text-medical-amber-600',
    bgColor: 'bg-medical-amber-100',
  },
];

export const FeaturesGrid: React.FC = () => {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <AnimatedSection animation="slide-up" className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Why MediChain AI?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Combining cutting-edge ASI Alliance technologies to deliver transparent, reliable medical diagnostics.
          </p>
        </AnimatedSection>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <AnimatedSection key={index} animation="slide-up" delay={index * 50}>
              <Card hover padding="lg" className="h-full">
                <div className={`w-12 h-12 ${feature.bgColor} rounded-xl flex items-center justify-center mb-4 ${feature.color}`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </Card>
            </AnimatedSection>
          ))}
        </div>
      </div>
    </section>
  );
};
