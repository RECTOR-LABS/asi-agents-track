'use client';

import React from 'react';
import { AlertTriangle, TrendingUp, Users } from 'lucide-react';
import { Card, AnimatedSection } from '../shared';

const statistics = [
  {
    icon: <TrendingUp className="w-8 h-8" />,
    value: '$40B',
    label: 'Annual cost of medical misdiagnosis in US',
    color: 'text-emergency-600',
    bgColor: 'bg-emergency-100',
  },
  {
    icon: <Users className="w-8 h-8" />,
    value: '12M',
    label: 'Americans affected by diagnostic errors yearly',
    color: 'text-urgent-600',
    bgColor: 'bg-urgent-100',
  },
  {
    icon: <AlertTriangle className="w-8 h-8" />,
    value: 'Thousands',
    label: 'Preventable deaths from misdiagnosis',
    color: 'text-medical-amber-600',
    bgColor: 'bg-medical-amber-100',
  },
];

export const ProblemStatement: React.FC = () => {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <AnimatedSection animation="slide-up" className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            The Problem We&apos;re Solving
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Medical misdiagnosis is a critical global challenge affecting millions and costing billions annually.
          </p>
        </AnimatedSection>

        <div className="grid md:grid-cols-3 gap-8">
          {statistics.map((stat, index) => (
            <AnimatedSection key={index} animation="scale-in" delay={index * 100}>
              <Card hover padding="lg" className="text-center h-full">
                <div className={`w-16 h-16 ${stat.bgColor} rounded-2xl flex items-center justify-center mx-auto mb-6 ${stat.color}`}>
                  {stat.icon}
                </div>
                <div className={`text-5xl font-bold mb-3 ${stat.color}`}>{stat.value}</div>
                <p className="text-gray-600 font-medium">{stat.label}</p>
              </Card>
            </AnimatedSection>
          ))}
        </div>
      </div>
    </section>
  );
};
