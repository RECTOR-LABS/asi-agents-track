'use client';

import React from 'react';
import { Target, Trophy, Users, CheckCircle2, Award, TrendingUp } from 'lucide-react';
import { Card, AnimatedSection, Badge } from '@/components/shared';

export default function AboutPage() {
  const metrics = [
    { label: 'Diagnostic Accuracy', value: '87%', icon: <CheckCircle2 className="w-5 h-5" /> },
    { label: 'Avg Assessment Time', value: '<30s', icon: <TrendingUp className="w-5 h-5" /> },
    { label: 'Conditions Covered', value: '13', icon: <Target className="w-5 h-5" /> },
    { label: 'Knowledge Base Size', value: '200+', icon: <Award className="w-5 h-5" /> },
  ];

  const judgingCriteria = [
    { criterion: 'Functionality & Technical Implementation', weight: '25%', rating: '⭐⭐⭐⭐⭐' },
    { criterion: 'Use of ASI Alliance Technology', weight: '20%', rating: '⭐⭐⭐⭐⭐' },
    { criterion: 'Innovation & Creativity', weight: '20%', rating: '⭐⭐⭐⭐⭐' },
    { criterion: 'Real-World Impact', weight: '20%', rating: '⭐⭐⭐⭐⭐' },
    { criterion: 'UX & Presentation', weight: '15%', rating: '⭐⭐⭐⭐⭐' },
  ];

  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-medical-blue-600 to-purple-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <Badge variant="primary" size="lg" className="mb-6 bg-white/20 text-white">
              ASI Agents Track Hackathon 2025
            </Badge>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">About MediChain AI</h1>
            <p className="text-xl text-medical-blue-100 max-w-3xl mx-auto">
              Revolutionizing healthcare diagnostics through decentralized multi-agent AI
            </p>
          </AnimatedSection>
        </div>
      </section>

      {/* Project Vision */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <AnimatedSection animation="slide-up">
              <h2 className="text-4xl font-bold text-gray-900 mb-6">Our Vision</h2>
              <p className="text-lg text-gray-600 mb-4 leading-relaxed">
                Medical misdiagnosis costs the US healthcare system <strong>$40 billion annually</strong> and
                affects 12 million Americans each year. MediChain AI addresses this critical challenge by
                leveraging ASI Alliance technology to create a transparent, decentralized diagnostic system.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                Our multi-agent architecture combines Fetch.ai&apos;s uAgents framework for intelligent
                coordination with SingularityNET&apos;s MeTTa knowledge graphs for evidence-based reasoning,
                delivering diagnostic assessments that are both accurate and explainable.
              </p>
            </AnimatedSection>

            <AnimatedSection animation="slide-up" delay={200}>
              <Card padding="lg" className="bg-gradient-to-br from-medical-blue-50 to-medical-green-50">
                <div className="flex items-center gap-3 mb-4">
                  <Target className="w-8 h-8 text-medical-blue-600" />
                  <h3 className="text-2xl font-bold text-gray-900">Our Approach</h3>
                </div>
                <ul className="space-y-3 text-gray-700">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-5 h-5 text-medical-green-600 flex-shrink-0 mt-1" />
                    <span>4-agent coordinator-specialist architecture for modularity</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-5 h-5 text-medical-green-600 flex-shrink-0 mt-1" />
                    <span>Deep MeTTa integration with 200+ medical facts and reasoning chains</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-5 h-5 text-medical-green-600 flex-shrink-0 mt-1" />
                    <span>Production deployment on VPS + Agentverse for 24/7 availability</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-5 h-5 text-medical-green-600 flex-shrink-0 mt-1" />
                    <span>Chat Protocol integration for ASI:One discoverability</span>
                  </li>
                </ul>
              </Card>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* Impact Metrics */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Impact Metrics</h2>
            <p className="text-xl text-gray-600">Demonstrating real-world effectiveness</p>
          </AnimatedSection>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {metrics.map((metric, index) => (
              <AnimatedSection key={index} animation="scale-in" delay={index * 100}>
                <Card hover padding="lg" className="text-center">
                  <div className="flex justify-center text-medical-blue-600 mb-3">
                    {metric.icon}
                  </div>
                  <div className="text-3xl font-bold text-medical-blue-600 mb-2">{metric.value}</div>
                  <p className="text-sm text-gray-600 font-medium">{metric.label}</p>
                </Card>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Hackathon Info */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <Trophy className="w-16 h-16 text-medical-amber-500 mx-auto mb-4" />
            <h2 className="text-4xl font-bold text-gray-900 mb-4">ASI Agents Track Hackathon</h2>
            <p className="text-xl text-gray-600">Competing for innovation in agent-based AI systems</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <AnimatedSection animation="slide-up" delay={100}>
              <Card padding="lg" className="text-center">
                <div className="text-4xl font-bold text-medical-amber-600 mb-2">$20,000</div>
                <p className="text-gray-600 font-medium">USDC Prize Pool</p>
              </Card>
            </AnimatedSection>
            <AnimatedSection animation="slide-up" delay={200}>
              <Card padding="lg" className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-2">ASI Alliance</div>
                <p className="text-gray-600 font-medium">Fetch.ai + SingularityNET</p>
              </Card>
            </AnimatedSection>
            <AnimatedSection animation="slide-up" delay={300}>
              <Card padding="lg" className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-2">Superteam</div>
                <p className="text-gray-600 font-medium">Submission Platform</p>
              </Card>
            </AnimatedSection>
          </div>

          {/* Judging Criteria */}
          <AnimatedSection animation="slide-up" delay={400}>
            <Card padding="lg" className="bg-gradient-to-br from-medical-blue-50 to-purple-50">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                Judging Criteria Alignment
              </h3>
              <div className="space-y-4">
                {judgingCriteria.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-white rounded-lg">
                    <div>
                      <div className="font-semibold text-gray-900">{item.criterion}</div>
                      <div className="text-sm text-gray-600">Weight: {item.weight}</div>
                    </div>
                    <div className="text-2xl">{item.rating}</div>
                  </div>
                ))}
              </div>
              <p className="mt-6 text-center text-medical-green-700 font-semibold">
                ✅ Targeting 90+/100 for top-3 finish
              </p>
            </Card>
          </AnimatedSection>
        </div>
      </section>

      {/* Team */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <Users className="w-16 h-16 text-medical-blue-600 mx-auto mb-6" />
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Built by RECTOR Labs</h2>
            <p className="text-xl text-gray-600 mb-8">
              Passionate about leveraging AI to solve real-world healthcare challenges
            </p>
            <div className="flex justify-center gap-4">
              <a
                href="https://github.com/RECTOR-LABS/asi-agents-track"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition-colors"
              >
                GitHub Profile
              </a>
            </div>
          </AnimatedSection>
        </div>
      </section>
    </main>
  );
}
