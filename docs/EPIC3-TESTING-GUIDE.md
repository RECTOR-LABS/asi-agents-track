# Epic 3 Testing Guide
## Symptom Analysis & Treatment Recommendation Agents

**Last Updated:** October 10, 2025 (Day 4)
**Status:** Ready for Testing
**Agents:** 5/5 Complete (100%)

---

## Table of Contents

1. [Pre-Testing Checklist](#pre-testing-checklist)
2. [Test Environment Setup](#test-environment-setup)
3. [Test Cases](#test-cases)
4. [Expected Results](#expected-results)
5. [Troubleshooting](#troubleshooting)

---

## Pre-Testing Checklist

### ✅ Before Starting Tests

- [ ] All 5 agents deployed to Agentverse
- [ ] All mailboxes created via Inspector
- [ ] All agent addresses in `.env` file
- [ ] Coordinator agent restarted with new addresses
- [ ] All agents showing "Active" status on Agentverse dashboard

### ✅ Environment Variables Required

```bash
# .env file must contain:
COORDINATOR_ADDRESS=agent1q...
PATIENT_INTAKE_ADDRESS=agent1q...
KNOWLEDGE_GRAPH_ADDRESS=agent1q...
SYMPTOM_ANALYSIS_ADDRESS=agent1q...         # NEW - Epic 3
TREATMENT_RECOMMENDATION_ADDRESS=agent1q...  # NEW - Epic 3
```

---

## Test Environment Setup

### Option 1: Agentverse Chat Interface (Recommended)

**Why:** Fastest way to test after deployment, no ASI:One indexing delay

**Steps:**
1. Visit agent profile: `https://agentverse.ai/agents/details/{COORDINATOR_ADDRESS}/profile`
2. Click chat interface link or use: `https://chat.agentverse.ai/sessions/{SESSION_ID}`
3. Send test messages
4. Monitor logs: `tail -f /tmp/*.log`

### Option 2: ASI:One Interface (Production-Like)

**Why:** Tests the full user experience as judges will see it

**Steps:**
1. Visit: https://asi1.ai/
2. Search for "medichain-coordinator" or `@medichain-coordinator`
3. Start conversation
4. Monitor logs: `tail -f /tmp/*.log`

**Note:** ASI:One may take 5-15 minutes to index new agents

---

## Test Cases

### Test Case 1: Emergency Scenario - Meningitis

**Objective:** Verify red flag detection and emergency classification

**Input:**
```
I have a severe headache, high fever, and my neck is very stiff.
I'm 28 years old.
```

**Expected Flow:**
1. Coordinator → Patient Intake Agent
2. Patient Intake → Coordinator (extracts: severe-headache, fever, neck-stiffness, age=28)
3. Coordinator → Symptom Analysis Agent
4. Symptom Analysis:
   - Detects **RED FLAG**: Meningitis triad
   - Urgency: **EMERGENCY**
   - Differential diagnosis: Meningitis (high confidence)
5. Coordinator → Treatment Recommendation Agent
6. Treatment Recommendation:
   - Treatments: IV antibiotics, hospitalization
   - Evidence sources: CDC guidelines
   - Specialist referral: Neurologist or ER immediately
   - Follow-up: Immediate (ER visit required)

**Expected Output:**
```
🔬 Symptom Analysis Complete

Urgency Level: EMERGENCY

🚨 RED FLAGS DETECTED:
  • Meningitis triad (headache + fever + neck stiffness)

Top Differential Diagnoses:
  1. meningitis (confidence: 90%+)

Recommended Action: 🚨 EMERGENCY: Call 911 or go to ER immediately...

═══════════════════════════════════
🏥 MEDICHAIN AI - DIAGNOSTIC REPORT
═══════════════════════════════════

PRIMARY ASSESSMENT: Meningitis

TREATMENT RECOMMENDATIONS:
  1. IV antibiotics (ceftriaxone or vancomycin)
     Evidence: CDC guidelines

👨‍⚕️ Specialist Referral: Neurologist or Infectious Disease Specialist (ER immediately)

📅 Follow-Up: Immediate (ER visit required)

⚠️ IMPORTANT DISCLAIMER
This is NOT medical advice...
```

**Pass Criteria:**
- ✅ Red flag detected
- ✅ Urgency = EMERGENCY
- ✅ Meningitis in top diagnosis
- ✅ ER recommendation clear
- ✅ Full report delivered
- ✅ <10 seconds total response time

---

### Test Case 2: Urgent Scenario - Pneumonia

**Objective:** Verify urgent classification and treatment recommendations

**Input:**
```
I've had a bad cough for 5 days, fever around 102°F,
and difficulty breathing. I'm 45 years old.
```

**Expected Flow:**
1-6. (Same multi-agent orchestration)

**Expected Output:**
- Urgency: **URGENT**
- Differential diagnosis: Pneumonia, COVID-19, Bronchitis
- Treatment: Antibiotics (amoxicillin), rest, hydration
- Evidence sources: CDC respiratory illness guidelines
- Specialist: Pulmonologist or Primary Care Physician
- Follow-up: Within 24 hours

**Pass Criteria:**
- ✅ Urgency = URGENT
- ✅ Pneumonia in differential
- ✅ Antibiotic treatment recommended
- ✅ 24-hour follow-up specified
- ✅ Evidence sources included

---

### Test Case 3: Routine Scenario - Common Cold

**Objective:** Verify routine classification and appropriate guidance

**Input:**
```
I have a runny nose, mild sore throat, and feel a bit tired.
Started yesterday. I'm 30 years old.
```

**Expected Flow:**
1-6. (Same multi-agent orchestration)

**Expected Output:**
- Urgency: **ROUTINE**
- Differential diagnosis: Common cold, early flu, allergies
- Treatment: Rest, fluids, OTC pain relievers
- Evidence sources: General medical guidelines
- Specialist: Primary Care Physician (if symptoms worsen)
- Follow-up: 1-2 weeks (or sooner if symptoms worsen)

**Pass Criteria:**
- ✅ Urgency = ROUTINE
- ✅ Common cold in differential
- ✅ Conservative treatment (rest, fluids)
- ✅ "If symptoms worsen" guidance
- ✅ No unnecessary urgency

---

### Test Case 4: Contraindication Detection - Allergy

**Objective:** Verify safety validation with patient allergies

**Input:**
```
I have a bad cough and chest pain. I'm allergic to penicillin.
I'm 50 years old.
```

**Expected Flow:**
1-6. (Same multi-agent orchestration)

**Expected Output:**
- Differential diagnosis: Pneumonia, bronchitis, etc.
- Treatment recommendations with **safety warnings**:
  - ⚠️ Caution: Patient has penicillin allergy. Verify [treatment] safety.
  - Alternative antibiotics suggested (azithromycin, fluoroquinolones)
- No penicillin-based antibiotics recommended

**Pass Criteria:**
- ✅ Allergy warning displayed
- ✅ Alternative treatments suggested
- ✅ Penicillin avoided in recommendations
- ✅ Safety-first approach

---

### Test Case 5: Multi-Symptom Differential Diagnosis

**Objective:** Verify differential diagnosis with ambiguous symptoms

**Input:**
```
I have a headache, nausea, and fatigue. It's been going on for 3 days.
I'm 35 years old.
```

**Expected Flow:**
1-6. (Same multi-agent orchestration)

**Expected Output:**
- Urgency: URGENT or ROUTINE (depending on severity interpretation)
- Differential diagnosis: Multiple conditions
  1. Migraine (40-60% confidence)
  2. Tension headache (30-50% confidence)
  3. Influenza (20-40% confidence)
  4. Gastroenteritis (20-40% confidence)
- Treatment: Varies based on primary diagnosis
- Specialist: Consider neurology if migraine suspected

**Pass Criteria:**
- ✅ Multiple diagnoses listed (2-5)
- ✅ Confidence scores shown
- ✅ Appropriate uncertainty handling
- ✅ Reasoning for each diagnosis
- ✅ No false confidence

---

### Test Case 6: Age-Based Risk Adjustment - Elderly

**Objective:** Verify age-specific safety considerations

**Input:**
```
I have chest pain and shortness of breath. I'm 72 years old.
```

**Expected Flow:**
1-6. (Same multi-agent orchestration)

**Expected Output:**
- Urgency: **EMERGENCY** (cardiac symptoms in elderly)
- Red flag: Chest pain (potential cardiac emergency)
- Differential: Heart attack, angina, pulmonary embolism
- Treatment:
  - **Contraindication note:** Age-over-65 cautions
  - Dose adjustment warnings for medications
- Specialist: Cardiologist (ER immediately)
- Follow-up: Immediate

**Pass Criteria:**
- ✅ Age-appropriate urgency escalation
- ✅ Geriatric cautions displayed
- ✅ Dose adjustment warnings
- ✅ Immediate ER recommendation

---

## Expected Results

### Performance Metrics

| Metric | Target | Acceptable | Notes |
|--------|--------|------------|-------|
| **Total Response Time** | <5s | <10s | Full diagnostic report |
| **Symptom Analysis Time** | <2s | <5s | From intake to analysis result |
| **Treatment Rec Time** | <2s | <5s | From analysis to treatment |
| **Accuracy** | 87%+ | 80%+ | Correct urgency + diagnosis |

### Success Criteria

**All Test Cases Must:**
- ✅ Complete without errors
- ✅ Generate full diagnostic report
- ✅ Display reasoning chains
- ✅ Include medical disclaimers
- ✅ Show evidence sources
- ✅ Detect red flags (where applicable)
- ✅ Check contraindications (where applicable)
- ✅ Recommend appropriate specialist

**Agent Communication Must:**
- ✅ Coordinator → Patient Intake → Coordinator
- ✅ Coordinator → Symptom Analysis → Coordinator
- ✅ Coordinator → Treatment Recommendation → Coordinator
- ✅ Coordinator → User (final report)
- ✅ All messages logged
- ✅ Session IDs match throughout

---

## Troubleshooting

### Issue: Agent Not Responding

**Symptoms:**
- Message sent, no response received
- Logs show "No active session found"

**Solutions:**
1. Check agent is running: `ps aux | grep python | grep agents`
2. Verify agent address in .env matches deployed agent
3. Check mailbox created: Visit agent profile on Agentverse
4. Restart coordinator to reload .env: `pkill -f coordinator.py && python src/agents/coordinator.py &`

---

### Issue: Incorrect Urgency Classification

**Symptoms:**
- Emergency symptoms classified as routine
- Routine symptoms classified as emergency

**Solutions:**
1. Check MeTTa knowledge base has urgency data: `grep "urgency-level" data/knowledge_base.metta`
2. Review red flag detection logic in symptom_analysis.py
3. Test MeTTa query directly: `python src/metta/query_engine.py`

---

### Issue: No Treatment Recommendations

**Symptoms:**
- Symptom analysis works, but no treatments provided
- "Unable to generate recommendations" error

**Solutions:**
1. Check treatment data in KB: `grep "has-treatment" data/knowledge_base.metta`
2. Verify Treatment Recommendation Agent is running
3. Check TREATMENT_RECOMMENDATION_ADDRESS in .env
4. Review logs: `tail -f /tmp/treatment_recommendation_deploy.log`

---

### Issue: Missing Contraindications

**Symptoms:**
- Allergies/age not considered
- No safety warnings displayed

**Solutions:**
1. Verify patient data passed correctly:
   - Check logs for "Patient age:", "Allergies:"
2. Check contraindication data in KB: `grep "contraindicated-with" data/knowledge_base.metta`
3. Verify message fields populated in coordinator routing

---

### Issue: Slow Response Time (>10 seconds)

**Symptoms:**
- Long delays between messages
- Timeout warnings in logs

**Solutions:**
1. Check MeTTa query performance: Add timing logs
2. Verify agents running on different ports (8000, 8001, 8003, 8004, 8005)
3. Check network latency to Agentverse
4. Consider local testing first before Agentverse

---

## Monitoring During Tests

### Recommended Terminal Setup (5 terminals)

**Terminal 1: Coordinator Logs**
```bash
tail -f /tmp/coordinator_mailbox.log
```

**Terminal 2: Patient Intake Logs**
```bash
tail -f /tmp/patient_intake_mailbox.log
```

**Terminal 3: Symptom Analysis Logs (NEW)**
```bash
tail -f /tmp/symptom_analysis_deploy.log
```

**Terminal 4: Treatment Recommendation Logs (NEW)**
```bash
tail -f /tmp/treatment_recommendation_deploy.log
```

**Terminal 5: Test Interface**
- Agentverse chat or ASI:One

### What to Look For in Logs

**✅ Successful Flow:**
```
[Coordinator] Received chat message from user...
[Coordinator] Routing to Patient Intake...
[Patient Intake] Received intake request...
[Patient Intake] Extracted symptoms: [fever, headache]
[Coordinator] Routing to Symptom Analysis Agent...
[Symptom Analysis] Analyzing 2 symptoms...
[Symptom Analysis] Urgency Assessment: EMERGENCY
[Coordinator] Received symptom analysis response...
[Coordinator] Routing to Treatment Recommendation Agent...
[Treatment Recommendation] Generating recommendations...
[Coordinator] Sending final diagnostic report to user...
```

**❌ Error Patterns:**
```
ERROR: No active session found
WARNING: Agent address not configured
ERROR: MeTTa query failed
WARNING: Timeout waiting for response
```

---

## Post-Testing

### After Successful Tests

1. **Document Results:**
   - Screenshot successful test cases
   - Save log snippets showing agent communication
   - Note response times

2. **Update Documentation:**
   - Mark test cases as passed in EXECUTION-PLAN.md
   - Update CLAUDE.md with final agent addresses
   - Add screenshots to docs/deployment/

3. **Prepare for Demo Video:**
   - Select best test case for demo (likely meningitis emergency)
   - Practice narration
   - Test screen recording setup

---

## Quick Test Script

For rapid testing after deployment:

```bash
#!/bin/bash
# quick_test.sh

echo "🧪 Quick Epic 3 Test"
echo ""

# Test 1: Check all agents running
echo "1️⃣ Checking agents..."
AGENTS=("coordinator" "patient_intake" "knowledge_graph" "symptom_analysis" "treatment_recommendation")

for agent in "${AGENTS[@]}"; do
    if ps aux | grep -q "[p]ython.*$agent"; then
        echo "   ✅ $agent running"
    else
        echo "   ❌ $agent NOT running"
    fi
done

echo ""

# Test 2: Verify .env has addresses
echo "2️⃣ Checking .env configuration..."
if grep -q "SYMPTOM_ANALYSIS_ADDRESS=agent1q" .env && ! grep -q "SYMPTOM_ANALYSIS_ADDRESS=agent1q\.\.\." .env; then
    echo "   ✅ SYMPTOM_ANALYSIS_ADDRESS configured"
else
    echo "   ❌ SYMPTOM_ANALYSIS_ADDRESS not configured"
fi

if grep -q "TREATMENT_RECOMMENDATION_ADDRESS=agent1q" .env && ! grep -q "TREATMENT_RECOMMENDATION_ADDRESS=agent1q\.\.\." .env; then
    echo "   ✅ TREATMENT_RECOMMENDATION_ADDRESS configured"
else
    echo "   ❌ TREATMENT_RECOMMENDATION_ADDRESS not configured"
fi

echo ""
echo "🎯 Ready to test! Use test cases from EPIC3-TESTING-GUIDE.md"
```

---

**Alhamdulillah! Testing guide complete. May Allah grant success in testing and demonstration!**
