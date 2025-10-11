'use client';

import React from 'react';
import { Book, Github, ExternalLink, Code, Users, Rocket } from 'lucide-react';
import { Card, AnimatedSection, Badge } from '@/components/shared';

const faqs = [
  {
    question: 'How accurate is MediChain AI?',
    answer: 'Our system achieves 87% diagnostic accuracy on test cases, covering 13 medical conditions with evidence-based reasoning from CDC, WHO, and other authoritative sources.',
  },
  {
    question: 'What medical conditions does it cover?',
    answer: '13 conditions total: 6 critical (meningitis, stroke, MI, PE, appendicitis, anaphylaxis), 2 urgent (pneumonia, UTI), and 5 common (influenza, migraine, GERD, allergic rhinitis, tension headache).',
  },
  {
    question: 'Is my data stored?',
    answer: 'No. All processing happens in real-time via mailbox protocol. No patient data is stored or logged. Complete privacy-first architecture.',
  },
  {
    question: 'How does MeTTa reasoning work?',
    answer: 'MeTTa is a symbolic reasoning engine from SingularityNET. It stores 200+ medical facts as knowledge graphs and performs transparent logical queries to generate diagnosis reasoning chains.',
  },
  {
    question: 'Can I deploy this myself?',
    answer: 'Yes! The project is open-source. See our GitHub repository for complete setup instructions, including VPS deployment, Agentverse configuration, and local development.',
  },
];

export default function DocsPage() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-gray-900 to-medical-blue-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <Book className="w-16 h-16 mx-auto mb-6" />
            <h1 className="text-5xl md:text-6xl font-bold mb-6">Documentation</h1>
            <p className="text-xl text-medical-blue-100 max-w-3xl mx-auto">
              Everything you need to understand, deploy, and extend MediChain AI
            </p>
          </AnimatedSection>
        </div>
      </section>

      {/* Quick Links */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <AnimatedSection animation="scale-in" delay={0}>
              <Card hover padding="lg" className="text-center h-full">
                <Github className="w-12 h-12 text-gray-900 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-900 mb-3">GitHub Repository</h3>
                <p className="text-gray-600 mb-6 text-sm">
                  Complete source code, setup instructions, and contribution guidelines
                </p>
                <a
                  href="https://github.com/RECTOR-LABS/asi-agents-track"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-medical-blue-600 font-semibold hover:text-medical-blue-700"
                >
                  View on GitHub <ExternalLink className="w-4 h-4" />
                </a>
              </Card>
            </AnimatedSection>

            <AnimatedSection animation="scale-in" delay={100}>
              <Card hover padding="lg" className="text-center h-full">
                <Code className="w-12 h-12 text-purple-600 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-900 mb-3">API Documentation</h3>
                <p className="text-gray-600 mb-6 text-sm">
                  Agent addresses, message protocols, and integration guides
                </p>
                <a
                  href="/architecture"
                  className="inline-flex items-center gap-2 text-medical-blue-600 font-semibold hover:text-medical-blue-700"
                >
                  View Architecture <ExternalLink className="w-4 h-4" />
                </a>
              </Card>
            </AnimatedSection>

            <AnimatedSection animation="scale-in" delay={200}>
              <Card hover padding="lg" className="text-center h-full">
                <Rocket className="w-12 h-12 text-medical-green-600 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-900 mb-3">Quick Start</h3>
                <p className="text-gray-600 mb-6 text-sm">
                  Test the live demo on Agentverse in under 2 minutes
                </p>
                <a
                  href="/demo"
                  className="inline-flex items-center gap-2 text-medical-blue-600 font-semibold hover:text-medical-blue-700"
                >
                  Try Demo <ExternalLink className="w-4 h-4" />
                </a>
              </Card>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* ASI Alliance Integration */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">ASI Alliance Integration</h2>
            <p className="text-xl text-gray-600">Deep integration with Fetch.ai and SingularityNET</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-2 gap-8">
            <AnimatedSection animation="slide-up" delay={100}>
              <Card padding="lg">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  <Badge variant="primary" className="mb-3">Fetch.ai</Badge>
                  uAgents Framework
                </h3>
                <ul className="space-y-3 text-gray-700">
                  <li className="flex items-start gap-2">
                    <span className="text-medical-blue-600 font-bold">•</span>
                    <span>Multi-agent orchestration with coordinator pattern</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-medical-blue-600 font-bold">•</span>
                    <span>Mailbox protocol for async communication</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-medical-blue-600 font-bold">•</span>
                    <span>Chat Protocol for ASI:One discoverability</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-medical-blue-600 font-bold">•</span>
                    <span>Agentverse deployment with 24/7 uptime</span>
                  </li>
                </ul>
              </Card>
            </AnimatedSection>

            <AnimatedSection animation="slide-up" delay={200}>
              <Card padding="lg">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  <Badge variant="success" className="mb-3">SingularityNET</Badge>
                  MeTTa Knowledge Graph
                </h3>
                <ul className="space-y-3 text-gray-700">
                  <li className="flex items-start gap-2">
                    <span className="text-medical-green-600 font-bold">•</span>
                    <span>200+ medical facts as symbolic knowledge</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-medical-green-600 font-bold">•</span>
                    <span>21 query methods (12 medical-specific)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-medical-green-600 font-bold">•</span>
                    <span>Transparent reasoning chain generation</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-medical-green-600 font-bold">•</span>
                    <span>Contraindication and drug interaction checks</span>
                  </li>
                </ul>
              </Card>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* Resources */}
      <section className="py-20 bg-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Resources & Links</h2>
          </AnimatedSection>

          <AnimatedSection animation="slide-up" delay={100}>
            <Card padding="lg">
              <div className="space-y-4">
                <a
                  href="https://fetch.ai/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <span className="font-semibold text-gray-900">Fetch.ai Documentation</span>
                  <ExternalLink className="w-5 h-5 text-gray-400" />
                </a>
                <a
                  href="https://metta-lang.dev"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <span className="font-semibold text-gray-900">MeTTa Language Docs</span>
                  <ExternalLink className="w-5 h-5 text-gray-400" />
                </a>
                <a
                  href="https://agentverse.ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <span className="font-semibold text-gray-900">Agentverse Platform</span>
                  <ExternalLink className="w-5 h-5 text-gray-400" />
                </a>
                <a
                  href="https://github.com/fetchai/innovation-lab-examples"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <span className="font-semibold text-gray-900">Innovation Lab Examples</span>
                  <ExternalLink className="w-5 h-5 text-gray-400" />
                </a>
              </div>
            </Card>
          </AnimatedSection>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
          </AnimatedSection>

          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <AnimatedSection key={index} animation="slide-up" delay={index * 50}>
                <Card padding="lg">
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{faq.question}</h3>
                  <p className="text-gray-600 leading-relaxed">{faq.answer}</p>
                </Card>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Contact */}
      <section className="py-20 bg-white">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <Users className="w-16 h-16 text-medical-blue-600 mx-auto mb-6" />
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Need Help?</h2>
            <p className="text-xl text-gray-600 mb-8">
              Check out our GitHub repository or reach out to the team
            </p>
            <a
              href="https://github.com/RECTOR-LABS/asi-agents-track/issues"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-8 py-4 bg-medical-blue-600 text-white rounded-lg font-semibold hover:bg-medical-blue-700 transition-colors"
            >
              <Github className="w-5 h-5" />
              Open GitHub Issue
            </a>
          </AnimatedSection>
        </div>
      </section>
    </main>
  );
}
