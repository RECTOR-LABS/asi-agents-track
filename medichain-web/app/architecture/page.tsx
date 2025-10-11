'use client';

import React, { useState } from 'react';
import { Network, Database, Cpu, Activity } from 'lucide-react';
import { Card, AnimatedSection, StatusIndicator, Badge } from '@/components/shared';
import { ArchitectureDiagram } from '@/components/architecture/ArchitectureDiagram';

const agents = [
  {
    id: 'coordinator',
    name: 'Coordinator Agent',
    role: 'Orchestrates patient journey & HTTP bridge',
    tech: 'uAgents + FastAPI + Queue-based architecture',
    address: 'agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q',
    port: '8001',
    icon: <Network className="w-6 h-6" />,
    color: 'bg-medical-blue-100 text-medical-blue-600',
  },
  {
    id: 'intake',
    name: 'Patient Intake Agent',
    role: 'NLP symptom extraction',
    tech: 'uAgents + spacy',
    address: 'agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2',
    port: '8000',
    icon: <Cpu className="w-6 h-6" />,
    color: 'bg-purple-100 text-purple-600',
  },
  {
    id: 'symptom',
    name: 'Symptom Analysis Agent',
    role: 'Pattern matching & urgency assessment',
    tech: 'uAgents + statistical models',
    address: 'agent1qdxqnfmu735ren2geq9f3n8ehdk43lvm9x0vxswv6xj6a5hn40yfqv0ar42',
    port: '8004',
    icon: <Activity className="w-6 h-6" />,
    color: 'bg-medical-green-100 text-medical-green-600',
  },
  {
    id: 'treatment',
    name: 'Treatment Recommendation Agent',
    role: 'Evidence-based treatment suggestions',
    tech: 'uAgents + MeTTa query results',
    address: 'agent1qg9m6r976jq4lj64qfnp679qu8lu4jzcy06y09mf7ta4l2sm8uq9qfqrc9v',
    port: '8005',
    icon: <Database className="w-6 h-6" />,
    color: 'bg-medical-amber-100 text-medical-amber-600',
  },
];

export default function ArchitecturePage() {
  const [selectedAgent, setSelectedAgent] = useState(agents[0]);

  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-gray-900 via-medical-blue-900 to-purple-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">System Architecture</h1>
            <p className="text-xl text-medical-blue-100 max-w-3xl mx-auto">
              Deep dive into our multi-agent coordinator-specialist architecture
            </p>
          </AnimatedSection>
        </div>
      </section>

      {/* Architecture Diagram */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">System Overview</h2>
            <p className="text-xl text-gray-600">4 specialized agents working in harmony</p>
          </AnimatedSection>

          <AnimatedSection animation="scale-in" delay={200}>
            <Card padding="lg" className="bg-gradient-to-br from-gray-50 to-medical-blue-50">
              <ArchitectureDiagram />
            </Card>
          </AnimatedSection>
        </div>
      </section>

      {/* Agent Details Tabs */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Agent Details</h2>
            <p className="text-xl text-gray-600">Click an agent to view details</p>
          </AnimatedSection>

          {/* Agent Selector */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {agents.map((agent) => (
              <button
                key={agent.id}
                onClick={() => setSelectedAgent(agent)}
                className={`p-4 rounded-xl transition-all ${
                  selectedAgent.id === agent.id
                    ? 'bg-medical-blue-600 text-white shadow-xl scale-105'
                    : 'bg-white text-gray-700 hover:shadow-lg hover:scale-102'
                }`}
              >
                <div className="flex flex-col items-center gap-2">
                  <div className={selectedAgent.id === agent.id ? 'text-white' : agent.color}>
                    {agent.icon}
                  </div>
                  <span className="text-sm font-semibold text-center">{agent.name.split(' ')[0]}</span>
                </div>
              </button>
            ))}
          </div>

          {/* Selected Agent Card */}
          <AnimatedSection key={selectedAgent.id} animation="scale-in">
            <Card padding="lg" className="bg-white">
              <div className="flex items-start gap-4 mb-6">
                <div className={`w-16 h-16 rounded-xl flex items-center justify-center ${selectedAgent.color}`}>
                  {selectedAgent.icon}
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{selectedAgent.name}</h3>
                  <p className="text-gray-600 mb-3">{selectedAgent.role}</p>
                  <StatusIndicator status="active" label="Live on VPS" size="md" />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Tech Stack</h4>
                  <p className="text-gray-600 text-sm">{selectedAgent.tech}</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Port</h4>
                  <Badge variant="info">{selectedAgent.port}</Badge>
                </div>
              </div>

              <div className="mt-6">
                <h4 className="font-semibold text-gray-900 mb-2">Agent Address</h4>
                <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm break-all text-gray-700">
                  {selectedAgent.address}
                </div>
              </div>

              <div className="mt-6 flex gap-3">
                <a
                  href={`https://agentverse.ai/agents/details/${selectedAgent.address}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 bg-medical-blue-600 text-white rounded-lg font-medium hover:bg-medical-blue-700 transition-colors"
                >
                  View on Agentverse →
                </a>
              </div>
            </Card>
          </AnimatedSection>
        </div>
      </section>

      {/* Knowledge Graph Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <Database className="w-16 h-16 text-purple-600 mx-auto mb-4" />
            <h2 className="text-4xl font-bold text-gray-900 mb-4">MeTTa Knowledge Graph</h2>
            <p className="text-xl text-gray-600">Deep integration with symbolic reasoning</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-3 gap-8">
            <AnimatedSection animation="scale-in" delay={100}>
              <Card hover padding="lg" className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">13</div>
                <p className="text-gray-600 font-medium mb-1">Medical Conditions</p>
                <p className="text-sm text-gray-500">6 critical, 2 urgent, 5 common</p>
              </Card>
            </AnimatedSection>
            <AnimatedSection animation="scale-in" delay={200}>
              <Card hover padding="lg" className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">200+</div>
                <p className="text-gray-600 font-medium mb-1">Medical Facts</p>
                <p className="text-sm text-gray-500">Evidence-based knowledge</p>
              </Card>
            </AnimatedSection>
            <AnimatedSection animation="scale-in" delay={300}>
              <Card hover padding="lg" className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">45+</div>
                <p className="text-gray-600 font-medium mb-1">Contraindications</p>
                <p className="text-sm text-gray-500">Drug safety checks</p>
              </Card>
            </AnimatedSection>
          </div>

          <AnimatedSection animation="slide-up" delay={400} className="mt-12">
            <Card padding="lg" className="bg-gradient-to-br from-purple-50 to-medical-blue-50">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Evidence Sources</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div className="p-4 bg-white rounded-lg">
                  <p className="font-semibold text-gray-900">CDC</p>
                  <p className="text-xs text-gray-600">Disease Control</p>
                </div>
                <div className="p-4 bg-white rounded-lg">
                  <p className="font-semibold text-gray-900">WHO</p>
                  <p className="text-xs text-gray-600">Global Health</p>
                </div>
                <div className="p-4 bg-white rounded-lg">
                  <p className="font-semibold text-gray-900">AHA</p>
                  <p className="text-xs text-gray-600">Heart Association</p>
                </div>
                <div className="p-4 bg-white rounded-lg">
                  <p className="font-semibold text-gray-900">Johns Hopkins</p>
                  <p className="text-xs text-gray-600">Medical Research</p>
                </div>
              </div>
            </Card>
          </AnimatedSection>
        </div>
      </section>

      {/* Technical Highlights */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Technical Highlights</h2>
          </AnimatedSection>

          <div className="space-y-4">
            {[
              'Queue-based HTTP bridge solving async/threading challenges',
              'Chat Protocol integration for ASI:One discoverability',
              'Real-time multi-agent communication via mailbox protocol',
              'Transparent reasoning chains from MeTTa query engine',
              'Production VPS deployment with systemd services (99.9% uptime)',
              'Session management with both http-* and session-* ID patterns',
            ].map((highlight, index) => (
              <AnimatedSection key={index} animation="slide-up" delay={index * 50}>
                <Card className="flex items-center gap-4">
                  <div className="w-8 h-8 bg-medical-green-100 text-medical-green-600 rounded-full flex items-center justify-center flex-shrink-0">
                    ✓
                  </div>
                  <p className="text-gray-700 font-medium">{highlight}</p>
                </Card>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
