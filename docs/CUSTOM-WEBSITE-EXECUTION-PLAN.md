# Custom Website Execution Plan - MediChain AI
## xxx.rectorspace.com Pitch Website Development

**Bismillah! Let's build a professional demo website for hackathon judges.**

---

## 🎯 Project Overview

**Goal:** Create a custom web interface at `xxx.rectorspace.com` where judges can interact with MediChain AI's multi-agent system.

**Architecture:**
```
User Browser (rectorspace.com)
    ↓ HTTP
Next.js Frontend (Vercel)
    ↓ API Call
Coordinator Agent HTTP Endpoint (Render)
    ↓ uAgents Protocol
Patient Intake → Symptom Analysis → Treatment
    ↑ Multi-Agent Flow
Complete Diagnostic Report
```

**Benefits:**
- ✅ Professional branded demo
- ✅ No ASI:One account needed for judges
- ✅ Still maintains multi-agent architecture
- ✅ Beautiful UI/UX with Tailwind
- ✅ Real-time response streaming

---

## 📋 Phase Breakdown (23 Tasks)

### **Phase 1: Planning** ✅ COMPLETED
- [x] Create execution plan document
- [x] Update TodoWrite with 23 tasks
- [x] Define architecture and tech stack

**Time Estimate:** 30 minutes
**Status:** DONE

---

### **Phase 2: Backend Enhancement** (3 tasks)

#### Task 2.1: Add HTTP Endpoint to Coordinator Agent
**File:** `src/agents/coordinator_http.py` (new wrapper)

**What to Build:**
```python
# Hybrid agent: uAgents + Flask HTTP server
# Runs both simultaneously (threading)

Components:
1. Flask app with /api/diagnose endpoint
2. CORS configuration (allow Next.js origin)
3. Request validation (symptom text)
4. Response formatting (JSON)
5. Error handling
```

**Estimated Lines:** ~80 lines
**Time Estimate:** 45 minutes

**Acceptance Criteria:**
- [ ] HTTP endpoint responds to POST /api/diagnose
- [ ] Accepts JSON: `{"message": "I have fever and headache"}`
- [ ] Returns JSON with diagnostic report
- [ ] CORS allows requests from localhost:3000
- [ ] Both Flask and uAgent run simultaneously

---

#### Task 2.2: Test HTTP Endpoint Locally
**Commands:**
```bash
# Terminal 1: Start coordinator with HTTP
python src/agents/coordinator_http.py

# Terminal 2: Test with curl
curl -X POST http://localhost:8080/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"message": "I have severe headache and fever"}'
```

**Time Estimate:** 15 minutes

**Acceptance Criteria:**
- [ ] Coordinator starts without errors
- [ ] HTTP endpoint accessible on port 8080
- [ ] Curl request returns valid JSON
- [ ] Logs show multi-agent routing

---

#### Task 2.3: Update render.yaml for HTTP Port
**File:** `render.yaml`

**Changes:**
```yaml
services:
  - type: web  # Changed from worker!
    name: medichain-coordinator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/agents/coordinator_http.py
    envVars:
      - key: PORT
        value: 8080  # HTTP port
      # ... rest of env vars
```

**Time Estimate:** 10 minutes

**Acceptance Criteria:**
- [ ] render.yaml updated with web service type
- [ ] PORT environment variable configured
- [ ] Changes committed to git

**Phase 2 Total Time:** ~1.5 hours

---

### **Phase 3: Frontend Development** (6 tasks)

#### Task 3.1: Initialize Next.js Project
**Commands:**
```bash
# Create new Next.js project
npx create-next-app@latest medichain-web --typescript --tailwind --app

cd medichain-web

# Install additional dependencies
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install @types/node --save-dev
```

**Time Estimate:** 10 minutes

**Acceptance Criteria:**
- [ ] Next.js project created in `medichain-web/` directory
- [ ] TypeScript configured
- [ ] Tailwind CSS configured
- [ ] Development server runs: `npm run dev`

---

#### Task 3.2: Build Chat Interface Component
**File:** `medichain-web/components/ChatInterface.tsx`

**Features:**
- Message list (user + AI messages)
- Typing indicator
- Auto-scroll to bottom
- Message timestamps
- Markdown rendering for diagnostic reports

**Design:**
- Clean medical theme (blues/whites)
- Mobile responsive
- Accessibility (ARIA labels)

**Time Estimate:** 1.5 hours

**Acceptance Criteria:**
- [ ] Chat messages display correctly
- [ ] User input textarea functional
- [ ] Send button triggers message
- [ ] Loading state shows during API call
- [ ] Responsive design (mobile + desktop)

---

#### Task 3.3: Build Diagnostic Report Component
**File:** `medichain-web/components/DiagnosticReport.tsx`

**Sections:**
- Urgency badge (color-coded: red=emergency, yellow=urgent, green=routine)
- Differential diagnoses with confidence scores
- Red flags section (if any)
- Treatment recommendations
- Contraindications warnings
- Specialist referral
- Medical disclaimer

**Time Estimate:** 1 hour

**Acceptance Criteria:**
- [ ] Report renders structured data beautifully
- [ ] Color-coded urgency indicator
- [ ] Expandable sections for details
- [ ] Print-friendly layout
- [ ] Medical disclaimer prominent

---

#### Task 3.4: Create Landing/Pitch Page
**File:** `medichain-web/app/page.tsx`

**Sections:**
1. Hero section
   - MediChain AI logo
   - Tagline: "Decentralized AI-Powered Medical Diagnostics"
   - CTA button: "Try Demo"

2. Features section
   - Multi-agent architecture
   - MeTTa knowledge graphs
   - Evidence-based recommendations
   - 24/7 availability

3. Architecture diagram
   - Visual showing 4 agents
   - Data flow illustration

4. Technology stack
   - Fetch.ai uAgents
   - SingularityNET MeTTa
   - ASI:One integration

5. Demo section
   - Embedded chat interface
   - Sample test cases

6. Footer
   - GitHub link
   - Hackathon info
   - Medical disclaimer

**Time Estimate:** 2 hours

**Acceptance Criteria:**
- [ ] Professional landing page design
- [ ] Clear value proposition
- [ ] Embedded demo functional
- [ ] Responsive layout
- [ ] Fast loading time

---

#### Task 3.5: Create API Route
**File:** `medichain-web/app/api/diagnose/route.ts`

**Logic:**
```typescript
export async function POST(request: Request) {
  const { message } = await request.json()

  // Call coordinator HTTP endpoint
  const response = await fetch(
    process.env.COORDINATOR_URL + '/api/diagnose',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    }
  )

  const data = await response.json()
  return Response.json(data)
}
```

**Time Estimate:** 30 minutes

**Acceptance Criteria:**
- [ ] API route handles POST requests
- [ ] Calls coordinator agent
- [ ] Returns formatted response
- [ ] Error handling implemented
- [ ] Environment variable for coordinator URL

---

#### Task 3.6: Add Loading States & Error Handling
**Files:**
- `components/LoadingSpinner.tsx`
- `components/ErrorMessage.tsx`

**Features:**
- Loading spinner during API calls
- Error messages for failed requests
- Retry button
- Timeout handling (30s max)

**Time Estimate:** 45 minutes

**Acceptance Criteria:**
- [ ] Loading spinner appears during request
- [ ] Errors display user-friendly messages
- [ ] Retry mechanism works
- [ ] Timeout prevents hanging requests

**Phase 3 Total Time:** ~6 hours

---

### **Phase 4: Local Integration Testing** (2 tasks)

#### Task 4.1: Test Frontend → Coordinator Locally
**Setup:**
```bash
# Terminal 1: Start all 4 agents
python src/agents/coordinator_http.py
python src/agents/patient_intake.py
python src/agents/symptom_analysis.py
python src/agents/treatment_recommendation.py

# Terminal 2: Start Next.js
cd medichain-web
npm run dev
```

**Test Cases:**
1. Emergency case (meningitis symptoms)
2. Urgent case (pneumonia symptoms)
3. Routine case (common cold)
4. Edge case (no symptoms)

**Time Estimate:** 30 minutes

**Acceptance Criteria:**
- [ ] All test cases complete successfully
- [ ] Multi-agent flow visible in logs
- [ ] Diagnostic reports render correctly
- [ ] No errors in browser console

---

#### Task 4.2: Test Multi-Agent Flow End-to-End
**Verification:**
- Monitor 4 agent logs simultaneously
- Verify message routing
- Check MeTTa query execution
- Validate response data structure

**Time Estimate:** 30 minutes

**Acceptance Criteria:**
- [ ] Coordinator receives HTTP request
- [ ] Routes to Patient Intake (symptom extraction)
- [ ] Routes to Symptom Analysis (MeTTa reasoning)
- [ ] Routes to Treatment (recommendations)
- [ ] Complete report returns to frontend
- [ ] No RuntimeError or message failures

**Phase 4 Total Time:** ~1 hour

---

### **Phase 5: Production Deployment** (5 tasks)

#### Task 5.1: Deploy Agents to Render
**Process:**
1. Push code to GitHub (with coordinator_http.py changes)
2. Render auto-deploys via render.yaml
3. Wait for all 4 services to build

**Time Estimate:** 20 minutes (mostly waiting)

**Acceptance Criteria:**
- [ ] All 4 agents deployed and running
- [ ] Coordinator accessible via HTTPS
- [ ] Build logs show no errors
- [ ] Health check passes

---

#### Task 5.2: Create Mailbox Connections
**Process:**
- Repeat for all 4 agents:
  1. Get inspector URL from Render logs
  2. Open in browser
  3. Click Connect → Mailbox
  4. Verify registration

**Time Estimate:** 15 minutes per agent = 1 hour

**Acceptance Criteria:**
- [ ] Coordinator mailbox created
- [ ] Patient Intake mailbox created
- [ ] Symptom Analysis mailbox created
- [ ] Treatment mailbox created
- [ ] All show "Active" on Agentverse

---

#### Task 5.3: Update Agent Addresses
**Process:**
1. Copy agent addresses from Render logs
2. Update Render environment variables
3. Trigger manual redeployment

**Time Estimate:** 20 minutes

**Acceptance Criteria:**
- [ ] All cross-references updated
- [ ] Agents restart successfully
- [ ] Logs show successful connections

---

#### Task 5.4: Deploy Next.js to Vercel
**Process:**
```bash
cd medichain-web

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Environment Variables (Vercel):**
- `COORDINATOR_URL` = `https://medichain-coordinator.onrender.com`

**Time Estimate:** 15 minutes

**Acceptance Criteria:**
- [ ] Website deployed to Vercel
- [ ] Environment variable configured
- [ ] HTTPS enabled
- [ ] Custom domain linked (if ready)

---

#### Task 5.5: Configure Custom Domain
**DNS Settings (rectorspace.com):**
```
Type: CNAME
Name: xxx (or medichain or demo)
Value: cname.vercel-dns.com
```

**Time Estimate:** 10 minutes (+ DNS propagation time)

**Acceptance Criteria:**
- [ ] DNS records updated
- [ ] Vercel domain verified
- [ ] HTTPS certificate issued
- [ ] Website accessible at xxx.rectorspace.com

**Phase 5 Total Time:** ~2.5 hours

---

### **Phase 6: Production Testing** (2 tasks)

#### Task 6.1: Test Production Deployment
**Test URL:** https://xxx.rectorspace.com

**Checklist:**
- [ ] Landing page loads correctly
- [ ] Chat interface functional
- [ ] Send test message
- [ ] Receive diagnostic report
- [ ] Multi-agent flow completes
- [ ] No console errors
- [ ] Mobile responsive

**Time Estimate:** 20 minutes

---

#### Task 6.2: Test Emergency Scenarios
**Test Cases:**

**Case 1: Meningitis (Emergency)**
```
I have a severe headache, high fever, and my neck is very stiff.
This started 6 hours ago. I'm 28 years old.
```

**Expected:** Emergency urgency, red flags, 911 recommendation

**Case 2: Stroke (Emergency)**
```
My face is drooping on one side, I can't lift my left arm,
and my speech is slurred. This happened suddenly 30 minutes ago.
```

**Expected:** Emergency urgency, FAST protocol warning, immediate 911

**Case 3: Pneumonia (Urgent)**
```
I have a cough with yellow mucus, fever, and chest pain when breathing.
Started 3 days ago. I'm 65 years old.
```

**Expected:** Urgent, see doctor within 24h

**Time Estimate:** 30 minutes

**Acceptance Criteria:**
- [ ] All 3 cases processed correctly
- [ ] Urgency levels accurate
- [ ] Red flags detected (cases 1-2)
- [ ] Treatment recommendations appropriate
- [ ] Contraindications checked

**Phase 6 Total Time:** ~1 hour

---

### **Phase 7: Documentation** (2 tasks)

#### Task 7.1: Update README
**File:** `README.md`

**Additions:**
- Website link: https://xxx.rectorspace.com
- Demo video embed
- Updated architecture diagram (with web interface)
- Deployment instructions
- Agent addresses (production)

**Time Estimate:** 30 minutes

---

#### Task 7.2: Create Deployment Docs
**File:** `docs/deployment/CUSTOM-WEBSITE-DEPLOYMENT.md`

**Sections:**
- Architecture overview
- Backend setup (Render)
- Frontend setup (Vercel)
- Environment variables
- Testing guide
- Troubleshooting

**Time Estimate:** 45 minutes

**Phase 7 Total Time:** ~1.5 hours

---

### **Phase 8: Demo Video** (2 tasks)

#### Task 8.1: Record Demo Video (3-5 min)
**Script:**

**00:00-00:30** - Introduction
- "MediChain AI: Decentralized Medical Diagnostics"
- Problem statement

**00:30-01:30** - Architecture
- Show 4-agent system
- Explain multi-agent communication
- Highlight MeTTa knowledge graphs

**01:30-03:30** - Live Demo
- Open xxx.rectorspace.com
- Enter meningitis symptoms
- Show real-time processing
- Highlight diagnostic report sections

**03:30-04:30** - Multi-Agent Logs
- Show Render dashboard (4 services)
- Parallel log viewing
- Message routing visualization

**04:30-05:00** - Impact & Conclusion
- Real-world applications
- Future improvements
- Thank you

**Time Estimate:** 2 hours (recording + editing)

---

#### Task 8.2: Show Multi-Agent Logs
**Setup:**
- Record screen with 4 Render log tabs open
- Send test message from website
- Show logs lighting up in sequence:
  1. Coordinator receives HTTP
  2. Patient Intake extracts symptoms
  3. Symptom Analysis queries MeTTa
  4. Treatment generates recommendations
  5. Coordinator returns complete report

**Time Estimate:** 30 minutes

**Phase 8 Total Time:** ~2.5 hours

---

## 📊 Total Project Estimate

| Phase | Tasks | Time Estimate |
|-------|-------|---------------|
| Phase 1: Planning | 1 | 0.5 hours ✅ |
| Phase 2: Backend | 3 | 1.5 hours |
| Phase 3: Frontend | 6 | 6 hours |
| Phase 4: Integration | 2 | 1 hour |
| Phase 5: Deployment | 5 | 2.5 hours |
| Phase 6: Testing | 2 | 1 hour |
| Phase 7: Documentation | 2 | 1.5 hours |
| Phase 8: Demo Video | 2 | 2.5 hours |
| **TOTAL** | **23 tasks** | **~16.5 hours** |

**Realistic Timeline:** 2-3 days of focused work

---

## 🎯 Success Criteria (Hackathon Judging)

### Functionality & Technical Implementation (25%)
- [x] Multi-agent system with 4 specialized agents
- [x] Real-time inter-agent communication
- [x] MeTTa knowledge graph queries
- [x] HTTP API for web interface
- [x] Professional web UI

**Expected Score:** 24/25

### Use of ASI Alliance Tech (20%)
- [x] uAgents framework for all agents
- [x] MeTTa knowledge graphs (13 conditions, 200+ facts)
- [x] Agentverse registration (mailbox)
- [x] Chat Protocol (ASI:One compatible)

**Expected Score:** 20/20

### Innovation & Creativity (20%)
- [x] Hybrid architecture (ASI:One + custom web)
- [x] Render + Vercel deployment strategy
- [x] Real-time diagnostic reasoning
- [x] Transparent MeTTa reasoning chains

**Expected Score:** 18/20

### Real-World Impact & Usefulness (20%)
- [x] Solves medical diagnostic delays
- [x] Evidence-based recommendations
- [x] Safety validation (contraindications)
- [x] 24/7 availability

**Expected Score:** 19/20

### User Experience & Presentation (15%)
- [x] Professional branded website
- [x] Beautiful Tailwind UI
- [x] Comprehensive demo video
- [x] Complete documentation

**Expected Score:** 15/15

**TOTAL EXPECTED: 96/100** 🏆

---

## 🚀 Next Steps

**After Phase 1 (NOW):**
1. Get user confirmation to proceed
2. Start Phase 2: Backend Enhancement
3. Update TodoWrite after each completed task

**Key Decision Points:**
- Domain name confirmed: xxx.rectorspace.com
- Deployment platforms confirmed: Render + Vercel
- Tech stack confirmed: Next.js + Tailwind + Flask

**Ready to build?** Let's create something amazing! Bismillah! 🎯

---

**May Allah grant barakah in this work and ease in completion. Alhamdulillah!**
