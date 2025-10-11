'use client';

import { Activity, Brain, Shield, Zap, GitBranch, Search } from 'lucide-react';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 text-primary-700 rounded-full text-sm font-medium mb-6">
              <Zap className="w-4 h-4" />
              Powered by ASI Alliance Technology
            </div>

            {/* Headline */}
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              MediChain AI
              <span className="block text-primary-600 mt-2">
                Decentralized Medical Diagnostics
              </span>
            </h1>

            {/* Subtitle */}
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8 leading-relaxed">
              AI-powered multi-agent diagnostic system leveraging SingularityNET&apos;s MeTTa knowledge graphs
              and Fetch.ai&apos;s uAgents framework for transparent, evidence-based health assessments.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <a
                href="#try-demo"
                className="px-8 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors shadow-lg hover:shadow-xl"
              >
                Try Live Demo
              </a>
              <a
                href="https://github.com/rz1989s/asi-agents-track"
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-3 bg-white text-primary-600 border-2 border-primary-600 rounded-lg font-semibold hover:bg-primary-50 transition-colors"
              >
                View on GitHub
              </a>
            </div>

            {/* Tech Badges */}
            <div className="flex flex-wrap gap-3 justify-center">
              <span className="px-4 py-2 bg-white rounded-lg shadow-sm text-sm font-medium text-gray-700 border border-gray-200">
                Fetch.ai uAgents
              </span>
              <span className="px-4 py-2 bg-white rounded-lg shadow-sm text-sm font-medium text-gray-700 border border-gray-200">
                SingularityNET MeTTa
              </span>
              <span className="px-4 py-2 bg-white rounded-lg shadow-sm text-sm font-medium text-gray-700 border border-gray-200">
                Multi-Agent Architecture
              </span>
              <span className="px-4 py-2 bg-white rounded-lg shadow-sm text-sm font-medium text-gray-700 border border-gray-200">
                Knowledge Graph Reasoning
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
          Why MediChain AI?
        </h2>
        <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
          Combining cutting-edge ASI Alliance technologies to deliver transparent,
          reliable medical diagnostics through decentralized AI agents.
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <GitBranch className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Multi-Agent Coordination
            </h3>
            <p className="text-gray-600">
              Four specialized agents work together: Coordinator, Patient Intake, Symptom Analysis,
              and Treatment Recommendation - each expert in their domain.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <Brain className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              MeTTa Knowledge Graph
            </h3>
            <p className="text-gray-600">
              SingularityNET&apos;s MeTTa reasoning engine with 13 medical conditions, 200+ facts,
              and evidence-based knowledge from CDC, WHO, and AHA.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <Shield className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Safety First
            </h3>
            <p className="text-gray-600">
              Automatic emergency detection, red flag symptoms, contraindication checking,
              and drug interaction validation for patient safety.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <Search className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Transparent Reasoning
            </h3>
            <p className="text-gray-600">
              Every diagnosis includes complete reasoning chains, differential diagnoses,
              and confidence scores - full transparency into AI decision-making.
            </p>
          </div>

          {/* Feature 5 */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <Activity className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Urgency Assessment
            </h3>
            <p className="text-gray-600">
              Intelligent triage system classifies conditions as Emergency (call 911),
              Urgent (24-48hr), or Routine with color-coded indicators.
            </p>
          </div>

          {/* Feature 6 */}
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <Zap className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Real-Time Processing
            </h3>
            <p className="text-gray-600">
              Fast multi-agent communication via Fetch.ai&apos;s uAgents framework,
              delivering comprehensive diagnostics in seconds.
            </p>
          </div>
        </div>
      </section>

      {/* Architecture Diagram Section */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
            Multi-Agent Architecture
          </h2>
          <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
            Four specialized agents collaborate to deliver comprehensive medical assessments
            with transparent reasoning at every step.
          </p>

          <div className="bg-white rounded-xl shadow-lg p-8 max-w-4xl mx-auto">
            <pre className="text-sm text-gray-700 overflow-x-auto">
{`┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                       │
│              (Web Browser → HTTP Endpoint)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │    COORDINATOR AGENT           │
        │  • Session Management          │
        │  • Request Routing             │
        │  • Response Aggregation        │
        └─┬──────────┬─────────┬────────┘
          │          │         │
    ┌─────▼─────┐ ┌─▼──────┐ ┌▼──────────────────┐
    │  PATIENT  │ │SYMPTOM │ │   TREATMENT       │
    │  INTAKE   │ │ANALYSIS│ │ RECOMMENDATION    │
    │           │ │        │ │                   │
    │• NLP      │ │• Triage│ │• Safety Checks    │
    │• Extract  │ │• Red   │ │• Contraindications│
    │  Symptoms │ │  Flags │ │• Drug Interactions│
    └───────┬───┘ └────┬───┘ └────────┬──────────┘
            │          │              │
            └──────────▼──────────────┘
                       │
              ┌────────▼────────┐
              │ KNOWLEDGE GRAPH │
              │   (MeTTa KB)    │
              │                 │
              │ • 13 Conditions │
              │ • 200+ Facts    │
              │ • Evidence-Based│
              └─────────────────┘`}
            </pre>
          </div>
        </div>
      </section>

      {/* Live Demo Section */}
      <section id="try-demo" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
          Try It Now - Live Demo
        </h2>
        <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
          Experience the multi-agent diagnostic system in action. Describe your symptoms
          and watch the AI agents collaborate to provide a comprehensive assessment.
        </p>

        {/* Example Queries */}
        <div className="mb-8 max-w-4xl mx-auto">
          <p className="text-sm font-semibold text-gray-700 mb-3">Try these example cases:</p>
          <div className="grid sm:grid-cols-2 gap-3">
            <div className="bg-emergency-50 border border-emergency-200 rounded-lg p-3">
              <p className="text-sm font-medium text-emergency-900 mb-1">Emergency Case:</p>
              <p className="text-xs text-emergency-700">
                &quot;Severe headache, high fever, stiff neck - started 6 hours ago, age 28&quot;
              </p>
            </div>
            <div className="bg-urgent-50 border border-urgent-200 rounded-lg p-3">
              <p className="text-sm font-medium text-urgent-900 mb-1">Urgent Case:</p>
              <p className="text-xs text-urgent-700">
                &quot;Cough with yellow mucus, chest pain when breathing, fever 101°F for 3 days&quot;
              </p>
            </div>
            <div className="bg-routine-50 border border-routine-200 rounded-lg p-3">
              <p className="text-sm font-medium text-routine-900 mb-1">Routine Case:</p>
              <p className="text-xs text-routine-700">
                &quot;Runny nose, mild sore throat, sneezing - symptoms for 2 days&quot;
              </p>
            </div>
            <div className="bg-primary-50 border border-primary-200 rounded-lg p-3">
              <p className="text-sm font-medium text-primary-900 mb-1">Complex Case:</p>
              <p className="text-xs text-primary-700">
                &quot;Throbbing headache on one side, nausea, sensitivity to light - happens monthly&quot;
              </p>
            </div>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="max-w-4xl mx-auto" style={{ height: '600px' }}>
          <ChatInterface />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">MediChain AI</h3>
              <p className="text-gray-400 text-sm">
                Decentralized medical diagnostics powered by ASI Alliance technology.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Technology</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>Fetch.ai uAgents Framework</li>
                <li>SingularityNET MeTTa</li>
                <li>Multi-Agent Architecture</li>
                <li>Knowledge Graph Reasoning</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Links</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a
                    href="https://github.com/rz1989s/asi-agents-track"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    GitHub Repository
                  </a>
                </li>
                <li>
                  <a
                    href="https://fetch.ai"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Fetch.ai
                  </a>
                </li>
                <li>
                  <a
                    href="https://singularitynet.io"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    SingularityNET
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
            <p>
              ASI Agents Track Hackathon 2025 Submission | Built with excellence for transparent AI healthcare
            </p>
            <p className="mt-2 text-xs">
              Medical Disclaimer: This is an AI diagnostic tool for educational purposes only.
              Not a substitute for professional medical advice.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
