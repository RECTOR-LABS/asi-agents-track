'use client';

import React, { useState } from 'react';
import { MessageSquare, Play, AlertTriangle, CheckCircle2, Brain, Shield, Activity, Database } from 'lucide-react';
import { Card, AnimatedSection, Button } from '@/components/shared';

// Comprehensive example cases showing all 25 conditions across different categories
const comprehensiveExamples = {
  emergency: [
    {
      condition: 'Meningitis',
      prompt: 'Severe headache, high fever 104°F, stiff neck, non-blanching rash - started 6 hours ago, age 28',
      expectedOutcome: 'Emergency classification, meningitis triad detection, immediate 911 guidance',
      icon: '🚨',
      badge: 'CRITICAL',
    },
    {
      condition: 'Stroke',
      prompt: 'Sudden weakness in left arm, face drooping on one side, slurred speech - age 65',
      expectedOutcome: 'FAST protocol detection, emergency classification, time-sensitive warning',
      icon: '🧠',
      badge: 'CRITICAL',
    },
    {
      condition: 'Heart Attack',
      prompt: 'Crushing chest pain radiating to left arm, shortness of breath, sweating - age 58, male',
      expectedOutcome: 'Cardiac emergency detection, troponin test recommendation, immediate ER',
      icon: '❤️',
      badge: 'CRITICAL',
    },
    {
      condition: 'Diabetic Ketoacidosis (DKA)',
      prompt: 'Extreme thirst, fruity breath smell, confusion, rapid breathing - diabetic, age 32',
      expectedOutcome: 'DKA detection, blood glucose/ketone tests, emergency insulin protocol',
      icon: '💉',
      badge: 'CRITICAL',
    },
    {
      condition: 'Anaphylaxis',
      prompt: 'Throat swelling, difficulty breathing, hives all over body - ate peanuts 5 min ago',
      expectedOutcome: 'Anaphylaxis detection, epinephrine administration, immediate 911',
      icon: '⚡',
      badge: 'CRITICAL',
    },
  ],
  urgent: [
    {
      condition: 'Pneumonia',
      prompt: 'Persistent cough with green mucus, fever 101°F, chest pain when breathing - 4 days, age 45',
      expectedOutcome: 'CURB-65 scoring, chest X-ray recommendation, antibiotic consideration',
      icon: '🫁',
      badge: 'URGENT',
    },
    {
      condition: 'Asthma Exacerbation',
      prompt: 'Severe wheezing, chest tightness, can\'t finish sentences - asthma history, age 25',
      expectedOutcome: 'Peak flow assessment, bronchodilator protocol, urgent care needed',
      icon: '😮‍💨',
      badge: 'URGENT',
    },
    {
      condition: 'Kidney Stones',
      prompt: 'Severe flank pain radiating to groin, blood in urine, nausea - age 40',
      expectedOutcome: 'Kidney stone suspicion, CT scan/ultrasound, urinalysis, pain management',
      icon: '💎',
      badge: 'URGENT',
    },
    {
      condition: 'Deep Vein Thrombosis (DVT)',
      prompt: 'Swollen left calf, warm to touch, pain when walking - recent long flight, age 52',
      expectedOutcome: 'Wells score calculation, D-dimer test, ultrasound doppler, PE risk',
      icon: '🦵',
      badge: 'URGENT',
    },
  ],
  routine: [
    {
      condition: 'Influenza',
      prompt: 'High fever, body aches, dry cough, extreme fatigue - symptoms for 2 days, age 35',
      expectedOutcome: 'Influenza vs COVID-19 differential, rest/hydration, antiviral timing',
      icon: '🤒',
      badge: 'ROUTINE',
    },
    {
      condition: 'Urinary Tract Infection (UTI)',
      prompt: 'Burning urination, frequent urge to pee, lower abdominal pain - female, age 29',
      expectedOutcome: 'UTI diagnosis, urinalysis recommendation, antibiotic options, hydration',
      icon: '🚽',
      badge: 'ROUTINE',
    },
    {
      condition: 'Migraine',
      prompt: 'Throbbing headache on left side, nausea, light sensitivity - happens monthly, age 32',
      expectedOutcome: 'Migraine pattern recognition, trigger identification, triptans consideration',
      icon: '💫',
      badge: 'ROUTINE',
    },
    {
      condition: 'Gastroenteritis',
      prompt: 'Diarrhea, nausea, stomach cramps, mild fever - ate seafood yesterday, age 38',
      expectedOutcome: 'Food poisoning vs gastroenteritis, hydration protocol, electrolyte replacement',
      icon: '🤢',
      badge: 'ROUTINE',
    },
  ],
};

// Input Validation Scenarios (Day 7 Feature)
const inputValidationExamples = [
  {
    category: '🚨 Emergency Detection',
    input: '"I have severe chest pain and can\'t breathe properly"',
    response: 'Immediate 911 guidance with emergency steps (DO NOT WAIT for analysis)',
    priority: 'CRITICAL',
    color: 'bg-red-50 border-red-300',
  },
  {
    category: '🆘 Mental Health Crisis',
    input: '"I\'m thinking about suicide, I can\'t take this anymore"',
    response: '988 Suicide Prevention Lifeline + Crisis Text Line resources (24/7 support)',
    priority: 'CRITICAL',
    color: 'bg-red-50 border-red-300',
  },
  {
    category: '⚠️ Prescription Request',
    input: '"Can you prescribe me antibiotics for my infection?"',
    response: 'Clear boundary: AI cannot prescribe, guide to licensed physician',
    priority: 'CRITICAL',
    color: 'bg-orange-50 border-orange-300',
  },
  {
    category: '👶 Proxy Symptoms (Children)',
    input: '"My 5-year-old daughter has high fever and won\'t stop crying"',
    response: 'Pediatric caution + symptom analysis (children deteriorate quickly)',
    priority: 'IMPORTANT',
    color: 'bg-yellow-50 border-yellow-300',
  },
  {
    category: '🤝 Greeting / Natural Language',
    input: '"Hey there! How are you doing today?"',
    response: 'Welcome message + guidance to describe medical symptoms',
    priority: 'UX',
    color: 'bg-blue-50 border-blue-300',
  },
  {
    category: '🐕 Pet Symptoms',
    input: '"My dog has been vomiting all morning"',
    response: 'Veterinary referral with compassion (not human healthcare)',
    priority: 'UX',
    color: 'bg-purple-50 border-purple-300',
  },
];

// System Capabilities Showcase
const systemCapabilities = [
  {
    title: '25 Medical Conditions',
    icon: <Database className="w-6 h-6" />,
    description: '9 Critical, 7 Urgent, 9 Routine conditions with comprehensive coverage',
    stat: '25 conditions',
    color: 'bg-medical-blue-600',
  },
  {
    title: '2,074 Medical Facts',
    icon: <Brain className="w-6 h-6" />,
    description: 'MeTTa Knowledge Graph v2.0 with evidence-based medical knowledge',
    stat: '2,074 KB lines',
    color: 'bg-purple-600',
  },
  {
    title: '14 Validation Scenarios',
    icon: <Shield className="w-6 h-6" />,
    description: 'Safety-first input validation: emergency, crisis, boundaries, UX',
    stat: '14 scenarios',
    color: 'bg-medical-green-600',
  },
  {
    title: '180 Risk Factors',
    icon: <Activity className="w-6 h-6" />,
    description: 'Risk-adjusted confidence scoring with age, history, attributes',
    stat: '180 factors',
    color: 'bg-orange-600',
  },
];

// Clinical Features
const clinicalFeatures = [
  {
    title: 'Clinical Scoring Systems',
    items: ['PERC Score (PE)', 'Wells Score (DVT/PE)', 'CURB-65 (Pneumonia)', 'CHA2DS2-VASc (Stroke)', 'GCS (Consciousness)', 'Centor (Strep Throat)'],
  },
  {
    title: 'Lab Test Recommendations',
    items: ['Blood Glucose', 'CBC', 'Troponin', 'D-Dimer', 'Urinalysis', 'ABG', 'Blood Cultures', 'Peak Flow'],
  },
  {
    title: 'Imaging Requirements',
    items: ['CT Scan', 'Chest X-Ray', 'Ultrasound', 'ECG', 'MRI', 'Ultrasound Doppler', 'Head CT'],
  },
  {
    title: 'Treatment Protocols',
    items: ['60 step-by-step protocols', 'Emergency timing', '83+ contraindications', 'Drug interactions', 'Evidence sources (CDC/WHO)'],
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
    title: 'Test Any Scenario',
    description: 'Use any example below - emergency, routine, validation, or your own',
  },
  {
    step: '4',
    title: 'Watch Multi-Agent Flow',
    description: '~15s response: Coordinator → Intake → Analysis → Treatment → Report',
  },
];

export default function DemoPage() {
  const [selectedCategory, setSelectedCategory] = useState<'emergency' | 'urgent' | 'routine'>('emergency');

  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-medical-green-600 to-medical-blue-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <Play className="w-16 h-16 mx-auto mb-6" />
            <h1 className="text-5xl md:text-6xl font-bold mb-6">Comprehensive Demo & Capabilities</h1>
            <p className="text-xl text-medical-green-100 max-w-3xl mx-auto mb-8">
              Test all 25 medical conditions, 14 input validation scenarios, and advanced clinical features.
              Built for ASI Agents Track Hackathon - Production-ready quality.
            </p>
            <div className="flex gap-4 justify-center flex-wrap">
              <Button
                variant="primary"
                size="lg"
                href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
                external
                className="!bg-white !text-medical-green-700 hover:!bg-medical-green-50 hover:scale-105 shadow-2xl border-4 border-medical-green-200"
              >
                <MessageSquare className="mr-2 w-5 h-5" />
                Test Live on Agentverse
              </Button>
              <Button
                variant="outline"
                size="lg"
                href="#capabilities"
                className="!border-white !text-white hover:!bg-white/10"
              >
                View All Capabilities ↓
              </Button>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* System Capabilities Overview */}
      <section id="capabilities" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">🏆 System Capabilities (Day 7 Complete)</h2>
            <p className="text-xl text-gray-600">Production-ready multi-agent diagnostic system with comprehensive safety</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {systemCapabilities.map((cap, index) => (
              <AnimatedSection key={index} animation="scale-in" delay={index * 100}>
                <Card className="h-full text-center hover:shadow-xl transition-all" padding="lg">
                  <div className={`w-16 h-16 ${cap.color} text-white rounded-full flex items-center justify-center mx-auto mb-4`}>
                    {cap.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{cap.stat}</h3>
                  <p className="font-semibold text-gray-800 mb-2">{cap.title}</p>
                  <p className="text-sm text-gray-600">{cap.description}</p>
                </Card>
              </AnimatedSection>
            ))}
          </div>

          {/* Clinical Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {clinicalFeatures.map((feature, index) => (
              <AnimatedSection key={index} animation="slide-up" delay={index * 100}>
                <Card className="h-full bg-gradient-to-br from-gray-50 to-blue-50" padding="lg">
                  <h4 className="font-bold text-gray-900 mb-3 text-lg">{feature.title}</h4>
                  <ul className="space-y-2">
                    {feature.items.map((item, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <CheckCircle2 className="w-4 h-4 text-medical-green-600 flex-shrink-0 mt-0.5" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </Card>
              </AnimatedSection>
            ))}
          </div>
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
                  and hackathon demonstration purposes only. It is <strong>NOT medical advice</strong> and should not replace
                  professional medical consultation. If you have a medical emergency, call 911 or visit your
                  nearest emergency room immediately. Always consult qualified healthcare professionals for
                  medical decisions.
                </p>
              </div>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* Comprehensive Medical Scenarios */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">🏥 Comprehensive Medical Scenarios</h2>
            <p className="text-xl text-gray-600">Test all 25 conditions across emergency, urgent, and routine categories</p>
          </AnimatedSection>

          {/* Category Selector */}
          <div className="flex justify-center gap-4 mb-8 flex-wrap">
            <button
              onClick={() => setSelectedCategory('emergency')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedCategory === 'emergency'
                  ? 'bg-red-600 text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              🚨 Emergency ({comprehensiveExamples.emergency.length})
            </button>
            <button
              onClick={() => setSelectedCategory('urgent')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedCategory === 'urgent'
                  ? 'bg-orange-600 text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              ⚠️ Urgent ({comprehensiveExamples.urgent.length})
            </button>
            <button
              onClick={() => setSelectedCategory('routine')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedCategory === 'routine'
                  ? 'bg-green-600 text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              🌡️ Routine ({comprehensiveExamples.routine.length})
            </button>
          </div>

          {/* Example Cards */}
          <div className="grid md:grid-cols-2 gap-6">
            {comprehensiveExamples[selectedCategory].map((example, index) => (
              <AnimatedSection key={index} animation="scale-in" delay={index * 100}>
                <Card
                  className={`border-2 hover:shadow-2xl transition-all ${
                    selectedCategory === 'emergency'
                      ? 'bg-red-50 border-red-300'
                      : selectedCategory === 'urgent'
                      ? 'bg-orange-50 border-orange-300'
                      : 'bg-green-50 border-green-300'
                  }`}
                  padding="lg"
                >
                  <div className="flex items-start gap-3 mb-4">
                    <span className="text-4xl">{example.icon}</span>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="font-bold text-xl text-gray-900">{example.condition}</h3>
                        <span className={`text-xs px-2 py-1 rounded font-semibold ${
                          selectedCategory === 'emergency'
                            ? 'bg-red-200 text-red-900'
                            : selectedCategory === 'urgent'
                            ? 'bg-orange-200 text-orange-900'
                            : 'bg-green-200 text-green-900'
                        }`}>
                          {example.badge}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="bg-white rounded-lg p-3">
                      <p className="text-xs font-semibold text-gray-600 mb-1">Test Input:</p>
                      <p className="text-sm italic text-gray-800">&quot;{example.prompt}&quot;</p>
                    </div>
                    <div className="bg-white rounded-lg p-3">
                      <p className="text-xs font-semibold text-gray-600 mb-1">Expected Output:</p>
                      <p className="text-sm text-gray-700">{example.expectedOutcome}</p>
                    </div>
                  </div>
                </Card>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Input Validation Scenarios (Day 7 Feature) */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              🛡️ Input Validation System <span className="text-medical-green-600">(Day 7 - NEW!)</span>
            </h2>
            <p className="text-xl text-gray-600">14 edge case scenarios with safety-first priority</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {inputValidationExamples.map((example, index) => (
              <AnimatedSection key={index} animation="slide-up" delay={index * 100}>
                <Card className={`border-2 ${example.color} hover:shadow-xl transition-all h-full`} padding="lg">
                  <div className="flex items-center gap-2 mb-3">
                    <h3 className="font-bold text-lg text-gray-900">{example.category}</h3>
                    <span className={`text-xs px-2 py-1 rounded font-semibold ${
                      example.priority === 'CRITICAL'
                        ? 'bg-red-200 text-red-900'
                        : example.priority === 'IMPORTANT'
                        ? 'bg-orange-200 text-orange-900'
                        : 'bg-blue-200 text-blue-900'
                    }`}>
                      {example.priority}
                    </span>
                  </div>
                  <div className="space-y-2">
                    <div className="bg-white rounded p-2">
                      <p className="text-xs font-semibold text-gray-600 mb-1">Input:</p>
                      <p className="text-sm italic text-gray-800">{example.input}</p>
                    </div>
                    <div className="bg-white rounded p-2">
                      <p className="text-xs font-semibold text-gray-600 mb-1">AI Response:</p>
                      <p className="text-sm text-gray-700">{example.response}</p>
                    </div>
                  </div>
                </Card>
              </AnimatedSection>
            ))}
          </div>

          <AnimatedSection animation="fade-in" delay={600} className="mt-8 text-center">
            <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200" padding="lg">
              <p className="text-gray-800">
                <strong>Total Coverage:</strong> 3 Critical (safety), 3 Important (UX+safety), 8 Nice-to-have (UX) = <strong className="text-medical-blue-600">14 validated scenarios</strong>
              </p>
            </Card>
          </AnimatedSection>
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

          <AnimatedSection animation="fade-in" delay={400} className="mt-12 text-center">
            <Button
              variant="primary"
              size="lg"
              href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
              external
              className="hover:scale-105 transition-transform shadow-2xl"
            >
              <MessageSquare className="mr-2 w-5 h-5" />
              Start Comprehensive Testing Now →
            </Button>
          </AnimatedSection>
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
              <div className="grid md:grid-cols-2 gap-4 mb-6">
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
                  <p className="text-lg font-bold text-medical-green-600">🟢 Live (24/7 VPS uptime)</p>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <p className="text-sm font-semibold text-gray-700 mb-1">Test Coverage:</p>
                  <p className="text-lg font-bold text-purple-600">181 tests passing ✅</p>
                </div>
              </div>
              <div className="bg-white rounded-lg p-4 mb-6">
                <p className="text-sm font-semibold text-gray-700 mb-2">Multi-Agent Architecture:</p>
                <p className="text-sm text-gray-600">
                  Coordinator → Patient Intake → Symptom Analysis → Treatment Recommendation → Comprehensive Report
                </p>
              </div>
              <div className="text-center">
                <Button
                  variant="primary"
                  size="lg"
                  href="https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"
                  external
                  className="hover:scale-105 transition-transform"
                >
                  Test All Capabilities Now →
                </Button>
              </div>
            </Card>
          </AnimatedSection>
        </div>
      </section>
    </main>
  );
}
