'use client';

import React from 'react';
import { MessageSquare, Play, AlertTriangle } from 'lucide-react';
import { Card, AnimatedSection, Button } from '@/components/shared';

const exampleCases = [
  {
    category: 'Emergency',
    prompt: 'Severe headache, high fever, stiff neck - started 6 hours ago, age 28',
    color: 'bg-emergency-50 border-emergency-200 text-emergency-900',
    icon: '🚨',
  },
  {
    category: 'Urgent',
    prompt: 'Cough with yellow mucus, chest pain when breathing, fever 101°F for 3 days',
    color: 'bg-urgent-50 border-urgent-200 text-urgent-900',
    icon: '⚠️',
  },
  {
    category: 'Routine',
    prompt: 'Runny nose, mild sore throat, sneezing - symptoms for 2 days',
    color: 'bg-routine-50 border-routine-200 text-routine-900',
    icon: '🌡️',
  },
  {
    category: 'Complex',
    prompt: 'Throbbing headache on one side, nausea, sensitivity to light - happens monthly',
    color: 'bg-medical-blue-50 border-medical-blue-200 text-medical-blue-900',
    icon: '🧠',
  },
];

const steps = [
  {
    step: '1',
    title: 'Navigate to Agentverse',
    description: 'Click the button below to access our Coordinator Agent on Agentverse',
  },
  {
    step: '2',
    title: 'Start Chat',
    description: 'On the agent profile page, click "Chat with Agent" button',
  },
  {
    step: '3',
    title: 'Describe Symptoms',
    description: 'Use one of the example cases or describe your own symptoms',
  },
  {
    step: '4',
    title: 'Receive Diagnosis',
    description: 'Watch the multi-agent system analyze and provide comprehensive assessment',
  },
];

export default function DemoPage() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-medical-green-600 to-medical-blue-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <Play className="w-16 h-16 mx-auto mb-6" />
            <h1 className="text-5xl md:text-6xl font-bold mb-6">Try Live Demo</h1>
            <p className="text-xl text-medical-green-100 max-w-3xl mx-auto mb-8">
              Experience MediChain AI in action. Test our multi-agent diagnostic system via Agentverse.
            </p>
            <Button
              variant="primary"
              size="lg"
              href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
              external
              className="!bg-white !text-medical-green-700 hover:!bg-medical-green-50 hover:scale-105 shadow-2xl border-4 border-medical-green-200"
            >
              <MessageSquare className="mr-2 w-5 h-5" />
              Open Agentverse Chat
            </Button>
          </AnimatedSection>
        </div>
      </section>

      {/* Medical Disclaimer */}
      <section className="py-12 bg-yellow-50 border-y border-yellow-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up">
            <div className="flex items-start gap-4">
              <AlertTriangle className="w-8 h-8 text-yellow-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-xl font-bold text-yellow-900 mb-2">⚠️ Medical Disclaimer</h3>
                <p className="text-yellow-800 leading-relaxed">
                  <strong>Important:</strong> MediChain AI is an AI-assisted diagnostic tool for educational
                  and research purposes only. It is <strong>NOT medical advice</strong> and should not replace
                  professional medical consultation. If you have a medical emergency, call 911 or visit your
                  nearest emergency room immediately. Always consult qualified healthcare professionals for
                  medical decisions.
                </p>
              </div>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* Example Cases */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Example Test Cases</h2>
            <p className="text-xl text-gray-600">Try these pre-formatted symptom descriptions</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-2 gap-6">
            {exampleCases.map((item, index) => (
              <AnimatedSection key={index} animation="scale-in" delay={index * 100}>
                <Card className={`border-2 ${item.color} hover:shadow-xl transition-all`} padding="lg">
                  <div className="flex items-start gap-3">
                    <span className="text-3xl">{item.icon}</span>
                    <div className="flex-1">
                      <h3 className="font-bold text-lg mb-2">{item.category} Case</h3>
                      <p className="text-sm italic">&quot;{item.prompt}&quot;</p>
                    </div>
                  </div>
                </Card>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* How to Test */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">How to Test</h2>
            <p className="text-xl text-gray-600">Follow these simple steps</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((item, index) => (
              <AnimatedSection key={index} animation="slide-up" delay={index * 100}>
                <Card hover padding="lg" className="h-full text-center">
                  <div className="w-12 h-12 bg-medical-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                    {item.step}
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{item.title}</h3>
                  <p className="text-gray-600 text-sm">{item.description}</p>
                </Card>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Agent Info */}
      <section className="py-20 bg-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up">
            <Card padding="lg" className="bg-gradient-to-br from-medical-blue-50 to-purple-50">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                🤖 Coordinator Agent Details
              </h3>
              <div className="space-y-4">
                <div className="bg-white rounded-lg p-4">
                  <p className="text-sm font-semibold text-gray-700 mb-1">Agent Address:</p>
                  <code className="text-xs text-gray-600 break-all">
                    agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q
                  </code>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <p className="text-sm font-semibold text-gray-700 mb-1">Average Response Time:</p>
                  <p className="text-lg font-bold text-medical-blue-600">~15 seconds</p>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <p className="text-sm font-semibold text-gray-700 mb-1">Status:</p>
                  <p className="text-lg font-bold text-medical-green-600">🟢 Live (24/7 uptime)</p>
                </div>
              </div>
              <div className="mt-6 text-center">
                <Button
                  variant="primary"
                  size="lg"
                  href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
                  external
                  className="hover:scale-105 transition-transform"
                >
                  Start Testing Now →
                </Button>
              </div>
            </Card>
          </AnimatedSection>
        </div>
      </section>
    </main>
  );
}
