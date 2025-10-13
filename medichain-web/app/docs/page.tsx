'use client';

import React, { useState } from 'react';
import { Book, Github, ExternalLink, Code, Users, Rocket, FileCode, Network, Terminal, Mail, Brain, Database, Bot, TestTube, Zap } from 'lucide-react';
import { Card, AnimatedSection, Badge, CodeBlock } from '@/components/shared';

const faqs = [
  {
    question: 'How accurate is MediChain AI?',
    answer: 'Our system achieves 87% diagnostic accuracy on test cases, covering 25 medical conditions with evidence-based reasoning from CDC, WHO, and other authoritative sources.',
  },
  {
    question: 'What medical conditions does it cover?',
    answer: '25 conditions total: 9 critical (meningitis, stroke, MI, PE, appendicitis, anaphylaxis, DKA, sepsis, aortic dissection), 7 urgent (pneumonia, asthma exacerbation, kidney stones, DVT, acute pancreatitis, cholecystitis, diverticulitis), and 9 routine (influenza, UTI, migraine, GERD, allergic rhinitis, tension headache, gastroenteritis, bronchitis, sinusitis).',
  },
  {
    question: 'Is my data stored?',
    answer: 'No. All processing happens in real-time via mailbox protocol. No patient data is stored or logged. Complete privacy-first architecture.',
  },
  {
    question: 'How does MeTTa reasoning work?',
    answer: 'MeTTa is a symbolic reasoning engine from SingularityNET. It stores 2,074 medical facts as knowledge graphs and performs transparent logical queries to generate diagnosis reasoning chains.',
  },
  {
    question: 'Can I deploy this myself?',
    answer: 'Yes! The project is open-source. See our GitHub repository for complete setup instructions, including VPS deployment, Agentverse configuration, and local development.',
  },
];

interface CodeExample {
  id: string;
  title: string;
  description: string;
  icon: React.ElementType;
  language: string;
  code: string;
  gradient: string;
}

const codeExamples: CodeExample[] = [
  {
    id: 'messageProtocol',
    title: 'Message Protocol',
    description: 'Pydantic models for inter-agent communication with type safety',
    icon: Mail,
    language: 'python',
    gradient: 'from-blue-500 to-cyan-500',
    code: `# Message Protocol Structure (Pydantic Models)

class Symptom(BaseModel):
    """Individual symptom with metadata"""
    name: str
    raw_text: str
    severity: Optional[int] = Field(None, ge=1, le=10)
    duration: Optional[str] = None
    frequency: Optional[str] = None

class PatientIntakeData(BaseModel):
    """Structured patient symptom data"""
    session_id: str
    symptoms: List[Symptom]
    age: Optional[int] = None
    medical_history: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None`,
  },
  {
    id: 'mettaQuery',
    title: 'MeTTa Queries',
    description: 'Symbolic reasoning engine with 34 query methods for diagnostics',
    icon: Brain,
    language: 'python',
    gradient: 'from-purple-500 to-pink-500',
    code: `# MeTTa Query Engine Examples

engine = MeTTaQueryEngine()

# Find conditions by symptom
conditions = engine.find_by_symptom("fever")
# Returns: ['meningitis', 'influenza', 'pneumonia', ...]

# Multi-symptom diagnostic matching
symptoms = ['fever', 'severe-headache', 'stiff-neck']
matches = engine.find_conditions_by_symptoms(symptoms)
# Returns: {'meningitis': 3, 'pneumonia': 1, 'influenza': 1}

# Get treatment recommendations
treatments = engine.find_treatment("meningitis")
# Returns: ['immediate-911', 'iv-antibiotics', 'lumbar-puncture']

# Check contraindications (Safety validation)
contraindicated = engine.check_contraindication(
    "aspirin", "bleeding-disorder"
)
# Returns: True

# Generate reasoning chain with transparency
reasoning = engine.generate_reasoning_chain(
    symptoms=['fever', 'severe-headache', 'stiff-neck'],
    top_condition='meningitis',
    patient_age=28
)
# Returns detailed step-by-step diagnostic reasoning`,
  },
  {
    id: 'knowledgeBase',
    title: 'Knowledge Base',
    description: '2,074 medical facts as symbolic knowledge graph',
    icon: Database,
    language: 'metta',
    gradient: 'from-green-500 to-emerald-500',
    code: `# Knowledge Base Structure (MeTTa Facts)

; Symptom relationships
(has-symptom meningitis fever)
(has-symptom meningitis severe-headache)
(has-symptom meningitis stiff-neck)
(has-symptom meningitis non-blanching-rash)

; Urgency levels
(has-urgency meningitis emergency)
(has-urgency influenza routine-care)

; Red flag symptoms
(red-flag-symptom stiff-neck true)
(red-flag-symptom non-blanching-rash true)

; Treatment recommendations
(has-treatment meningitis immediate-911)
(has-treatment meningitis iv-antibiotics)

; Safety validation
(contraindication aspirin bleeding-disorder)
(contraindication aspirin pregnancy-third-trimester)
(drug-interaction aspirin warfarin)

; Lab tests & imaging (Epic 7)
(requires-lab-test diabetic-ketoacidosis blood-glucose)
(requires-imaging kidney-stones ct-scan)`,
  },
  {
    id: 'agentImplementation',
    title: 'Agent Code',
    description: 'Multi-agent coordinator with Chat Protocol for ASI:One',
    icon: Bot,
    language: 'python',
    gradient: 'from-orange-500 to-red-500',
    code: `# Coordinator Agent with Chat Protocol

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, ChatAcknowledgement, chat_protocol_spec
)

agent = Agent(
    name="medichain_coordinator",
    seed="your_secure_seed",
    mailbox=True,  # Enable Agentverse mailbox
    port=8000
)

# Include Chat Protocol for ASI:One discovery
chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received from {sender}: {msg.content}")

    # Process symptom text
    for item in msg.content:
        if hasattr(item, 'text'):
            symptoms = extract_symptoms(item.text)
            diagnosis = await analyze_symptoms(symptoms)

            # Send response
            await ctx.send(sender, ChatAcknowledgement())

agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()`,
  },
  {
    id: 'testing',
    title: 'Testing',
    description: 'Comprehensive test suite with 181 passing tests',
    icon: TestTube,
    language: 'python',
    gradient: 'from-indigo-500 to-blue-500',
    code: `# Comprehensive Test Suite (181 tests passing)

# Test MeTTa Query Engine
def test_emergency_condition_detection():
    engine = MeTTaQueryEngine()
    emergencies = engine.find_emergency_conditions()
    assert 'meningitis' in emergencies
    assert 'stroke' in emergencies
    assert 'heart-attack' in emergencies

# Test Multi-Agent Integration
async def test_coordinator_to_intake_flow():
    coordinator = CoordinatorAgent()
    intake = PatientIntakeAgent()

    # Send symptom text
    response = await coordinator.process_user_input(
        "Severe headache, high fever, stiff neck - age 28"
    )

    assert response.urgency_level == "emergency"
    assert "meningitis" in response.possible_conditions

# Test Input Validation (14 scenarios)
def test_emergency_detection_validation():
    result = validate_input("I have severe chest pain and can't breathe")
    assert result.category == "emergency_detection"
    assert result.priority == "CRITICAL"
    assert "911" in result.response.lower()`,
  },
  {
    id: 'deployment',
    title: 'Deployment',
    description: 'VPS + Agentverse deployment with 24/7 uptime',
    icon: Zap,
    language: 'bash',
    gradient: 'from-yellow-500 to-orange-500',
    code: `# Deployment Instructions

## VPS Deployment (Production)

# 1. Install dependencies
sudo apt update
pip install -r requirements.txt

# 2. Configure systemd services
sudo cp deploy/medichain-coordinator.service /etc/systemd/system/
sudo systemctl enable medichain-coordinator
sudo systemctl start medichain-coordinator

# 3. Verify status
sudo systemctl status medichain-coordinator
sudo journalctl -u medichain-coordinator -f

## Agentverse Configuration

# 1. Create mailbox via inspector
python src/agents/coordinator.py  # Start agent
# Click "Connect" in inspector URL
# Select "Mailbox" → "OK, got it"

# 2. Verify registration
# Check logs: "Successfully registered as mailbox agent"
# Dashboard: https://agentverse.ai/agents

## Local Testing

# Start all agents in separate terminals
python src/agents/coordinator.py              # Port 8000
python src/agents/patient_intake.py           # Port 8001
python src/agents/symptom_analysis.py         # Port 8004
python src/agents/treatment_recommendation.py # Port 8005

# Run tests
pytest tests/ --cov=src`,
  },
];


const architectureDetails = [
  {
    title: 'Agent Communication Flow',
    description: 'Mailbox Protocol enables async inter-agent messaging through Agentverse infrastructure',
    tech: 'uAgents mailbox=True, Pydantic message models, Chat Protocol for ASI:One',
  },
  {
    title: 'MeTTa Knowledge Graph',
    description: '2,074 medical facts with 34 query methods for transparent diagnostic reasoning',
    tech: 'hyperon>=0.1.0, symbolic reasoning, multi-hop queries, evidence tracing',
  },
  {
    title: 'Input Validation System',
    description: '14 edge case scenarios with safety-first priority (emergency, crisis, boundaries)',
    tech: 'Confidence scoring, priority-based validation, flexible NLP detection',
  },
  {
    title: 'Testing Infrastructure',
    description: '181 comprehensive tests covering all components and medical scenarios',
    tech: 'pytest, pytest-asyncio, 84% coverage, zero critical bugs',
  },
];

export default function DocsPage() {
  const [selectedExampleIndex, setSelectedExampleIndex] = useState(0);
  const selectedExample = codeExamples[selectedExampleIndex] ?? codeExamples[0]!;

  // Early return if no examples (defensive coding)
  if (!selectedExample) {
    return null;
  }

  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-gray-900 to-medical-blue-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection animation="fade-in">
            <Book className="w-16 h-16 mx-auto mb-6" />
            <h1 className="text-5xl md:text-6xl font-bold mb-6">Comprehensive Documentation</h1>
            <p className="text-xl text-medical-blue-100 max-w-3xl mx-auto">
              Everything you need to understand, deploy, and extend MediChain AI - with complete code examples and implementation details
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

      {/* Code Examples Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-16">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-6 shadow-lg">
              <FileCode className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-5xl font-bold text-gray-900 mb-4">
              Code Examples & Implementation
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Explore production-ready code snippets from our multi-agent diagnostic system
            </p>
          </AnimatedSection>

          {/* Code Example Tab Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
            {codeExamples.map((example, index) => {
              const Icon = example.icon;
              const isSelected = selectedExampleIndex === index;

              return (
                <AnimatedSection key={example.id} animation="scale-in" delay={index * 50}>
                  <button
                    onClick={() => setSelectedExampleIndex(index)}
                    className={`w-full text-left p-6 rounded-2xl transition-all duration-300 ${
                      isSelected
                        ? 'bg-white shadow-2xl scale-105 ring-2 ring-medical-blue-500/50'
                        : 'bg-white/60 backdrop-blur shadow-md hover:shadow-xl hover:scale-102'
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <div
                        className={`flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center bg-gradient-to-br ${example.gradient} shadow-lg`}
                      >
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3
                          className={`text-lg font-bold mb-1 transition-colors ${
                            isSelected ? 'text-gray-900' : 'text-gray-800'
                          }`}
                        >
                          {example.title}
                        </h3>
                        <p className="text-sm text-gray-600 line-clamp-2">
                          {example.description}
                        </p>
                      </div>
                    </div>

                    {isSelected && (
                      <div className="mt-4 flex items-center gap-2 text-medical-blue-600">
                        <div className="w-1.5 h-1.5 rounded-full bg-medical-blue-600 animate-pulse"></div>
                        <span className="text-sm font-semibold">Currently viewing</span>
                      </div>
                    )}
                  </button>
                </AnimatedSection>
              );
            })}
          </div>

          {/* Code Display */}
          <AnimatedSection key={selectedExample.id} animation="fade-in">
            <CodeBlock
              code={selectedExample.code}
              language={selectedExample.language}
              title={selectedExample.title}
              showLineNumbers={false}
            />
          </AnimatedSection>

          {/* Stats below code */}
          <AnimatedSection animation="slide-up" delay={200}>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-8 text-center">
              <div className="flex items-center gap-2">
                <Code className="w-5 h-5 text-blue-600" />
                <span className="text-gray-700">
                  <span className="font-bold text-gray-900">2,000+</span> lines of code
                </span>
              </div>
              <div className="flex items-center gap-2">
                <TestTube className="w-5 h-5 text-green-600" />
                <span className="text-gray-700">
                  <span className="font-bold text-gray-900">181</span> tests passing
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-600" />
                <span className="text-gray-700">
                  <span className="font-bold text-gray-900">4</span> deployed agents
                </span>
              </div>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* Architecture Details */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <Network className="w-16 h-16 text-purple-600 mx-auto mb-4" />
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Technical Architecture</h2>
            <p className="text-xl text-gray-600">Deep dive into system components</p>
          </AnimatedSection>

          <div className="grid md:grid-cols-2 gap-8">
            {architectureDetails.map((detail, index) => (
              <AnimatedSection key={index} animation="scale-in" delay={index * 100}>
                <Card padding="lg" className="h-full bg-gradient-to-br from-gray-50 to-blue-50 hover:shadow-xl transition-all">
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{detail.title}</h3>
                  <p className="text-gray-700 mb-4">{detail.description}</p>
                  <div className="bg-white rounded-lg p-3">
                    <p className="text-sm text-gray-600 font-mono">{detail.tech}</p>
                  </div>
                </Card>
              </AnimatedSection>
            ))}
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
                    <span>2,074 medical facts as symbolic knowledge</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-medical-green-600 font-bold">•</span>
                    <span>34 query methods (16 medical-specific)</span>
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

      {/* System Statistics */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection animation="slide-up" className="text-center mb-12">
            <Terminal className="w-16 h-16 text-medical-green-600 mx-auto mb-4" />
            <h2 className="text-4xl font-bold text-gray-900 mb-4">System Capabilities</h2>
            <p className="text-xl text-gray-600">Production-ready multi-agent diagnostic system</p>
          </AnimatedSection>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { label: 'Medical Conditions', value: '25', color: 'bg-blue-50 text-blue-600' },
              { label: 'Medical Facts', value: '2,074', color: 'bg-purple-50 text-purple-600' },
              { label: 'Query Methods', value: '34', color: 'bg-green-50 text-green-600' },
              { label: 'Tests Passing', value: '181', color: 'bg-orange-50 text-orange-600' },
              { label: 'Contraindications', value: '83+', color: 'bg-red-50 text-red-600' },
              { label: 'Lab Tests', value: '37+', color: 'bg-indigo-50 text-indigo-600' },
              { label: 'Imaging Types', value: '12', color: 'bg-pink-50 text-pink-600' },
              { label: 'Risk Factors', value: '180', color: 'bg-yellow-50 text-yellow-600' },
            ].map((stat, index) => (
              <AnimatedSection key={index} animation="scale-in" delay={index * 50}>
                <Card padding="lg" className={`text-center ${stat.color}`}>
                  <div className="text-3xl font-bold mb-2">{stat.value}</div>
                  <div className="text-sm font-medium">{stat.label}</div>
                </Card>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Resources */}
      <section className="py-20 bg-gray-50">
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
      <section className="py-20 bg-white">
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
      <section className="py-20 bg-gray-50">
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
