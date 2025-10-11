# MediChain AI - Demo & Testing Checklist

**Before Recording Demo Video** ✅

---

## Pre-Demo Checks (5 minutes)

### 1. VPS Backend Health ✅
```bash
# Quick health check
curl http://176.222.53.185:8080/health

# Expected: {"status": "healthy", "agent": "medichain-coordinator", ...}
```

### 2. All Services Running ✅
```bash
ssh website 'sudo systemctl status medichain-*.service | grep "Active:"'

# Expected: All show "Active: active (running)"
```

### 3. Frontend Loading ✅
- Open: https://medichain-web.vercel.app
- Should load within 2-3 seconds
- Landing page displays correctly
- Chat interface visible at bottom

---

## Manual Test Cases (Test Before Recording!)

### Test Case 1: Routine Condition ✅

**Input:**
```
I have a severe headache and fever for 2 days
```

**Expected Response (10-15 seconds):**
- ✅ Urgency Badge: **ROUTINE** (Green)
- ✅ Differential Diagnoses: Influenza, COVID-19
- ✅ Confidence Scores: ~15-20% each
- ✅ Treatment: Antivirals, rest, fluids
- ✅ Specialist: Primary Care Physician
- ✅ Medical Disclaimer: Present

**Screenshot Locations:**
- Urgency badge (top of response)
- Differential diagnoses list
- Treatment recommendations

---

### Test Case 2: Emergency Condition 🚨

**Input:**
```
Severe headache, high fever, stiff neck - started 6 hours ago, age 28
```

**Expected Response:**
- ✅ Urgency Badge: **EMERGENCY** (Red)
- ✅ Red Flags: Detected (stiff neck, sudden onset)
- ✅ Action: "🚨 EMERGENCY: Call 911 immediately"
- ✅ Differential Diagnosis: Meningitis
- ✅ Time Sensitivity Warning: Present

**Key Highlight:**
- **RED urgency badge** - Most dramatic for demo video!

---

### Test Case 3: Urgent Condition ⚠️

**Input:**
```
Cough with yellow mucus, chest pain when breathing, fever 101°F for 3 days
```

**Expected Response:**
- ✅ Urgency Badge: **URGENT** (Orange)
- ✅ Differential Diagnosis: Pneumonia
- ✅ Action: "Seek medical attention within 24-48 hours"
- ✅ Treatment: Antibiotics (with contraindications)

---

### Test Case 4: Common Condition 📋

**Input:**
```
Runny nose, mild sore throat, sneezing - symptoms for 2 days
```

**Expected Response:**
- ✅ Urgency Badge: **ROUTINE** (Green)
- ✅ Differential Diagnosis: Common Cold
- ✅ Treatment: Rest, fluids, symptom management
- ✅ Self-care focus

---

## Demo Video Structure (3-5 minutes)

### Script Timeline:

**0:00-0:30 | Problem Statement**
- "Healthcare diagnostics are expensive and inaccessible"
- "AI can help triage, but lacks transparency"
- "Enter MediChain AI..."

**0:30-1:00 | Solution Overview**
- "Multi-agent system with 4 specialized agents"
- "MeTTa knowledge graph for reasoning"
- "Transparent, evidence-based diagnostics"

**1:00-2:00 | Architecture**
- Show architecture diagram (from landing page)
- Explain agent roles:
  - Patient Intake (NLP)
  - Symptom Analysis (Triage)
  - Treatment Recommendation (Safety)
  - Coordinator (Orchestration)
- Mention MeTTa KB: 200+ facts, 13 conditions

**2:00-4:00 | Live Demo** ⭐ **MOST IMPORTANT**
1. Open https://medichain-web.vercel.app
2. Scroll to demo section
3. Test **Emergency Case First** (most impressive!):
   - Input: Meningitis symptoms
   - Show RED urgency badge
   - Highlight "Call 911 immediately"
   - Point out red flags detection
4. Test Routine Case (show contrast):
   - Input: Headache + fever
   - Show GREEN routine badge
   - Highlight differential diagnoses
   - Show confidence scores

**4:00-4:30 | Technical Highlights**
- "4 agents communicating via Fetch.ai uAgents"
- "MeTTa knowledge graph with 200+ medical facts"
- "Transparent reasoning: see confidence scores, differential diagnoses"
- "Safety-first: contraindication checking, drug interactions"

**4:30-5:00 | Impact & Scalability**
- "24/7 triage assistance"
- "Reduces healthcare burden"
- "Scalable to thousands of conditions"
- "Open for expansion and collaboration"

---

## Recording Checklist

### Before Recording:
- [ ] Test all 4 cases manually (verify they work)
- [ ] Close unnecessary browser tabs
- [ ] Clear browser history (for clean demo)
- [ ] Prepare script or talking points
- [ ] Test microphone audio
- [ ] Set screen resolution to 1920x1080
- [ ] Hide personal information (bookmarks, etc.)

### During Recording:
- [ ] Speak clearly and confidently
- [ ] Show cursor movements smoothly
- [ ] Pause briefly after each key point
- [ ] Smile (if showing face)
- [ ] Show enthusiasm!

### After Recording:
- [ ] Watch entire video once
- [ ] Check audio quality
- [ ] Verify all test cases shown correctly
- [ ] Add title card (optional)
- [ ] Upload to YouTube/Vimeo
- [ ] Set to Public/Unlisted

---

## Quick Troubleshooting

### If Something Goes Wrong During Demo:

**Backend Not Responding:**
```bash
# Check services
ssh website 'sudo systemctl restart medichain-*.service'
# Wait 10 seconds, try again
```

**Frontend Error:**
- Refresh page (Cmd/Ctrl + R)
- Clear cache (Cmd/Ctrl + Shift + R)
- Try incognito mode

**Slow Response (> 30s):**
- Check VPS load: `ssh website 'htop'`
- Restart coordinator: `ssh website 'sudo systemctl restart medichain-coordinator.service'`

---

## Post-Demo Submission Checklist

After recording demo video:

- [ ] Upload video to YouTube
- [ ] Update README.md with video link
- [ ] Update README with production URLs
- [ ] Commit and push final changes
- [ ] Submit to earn.superteam.fun
- [ ] Celebrate! 🎉

---

## Production URLs (For Reference)

**Frontend:** https://medichain-web.vercel.app
**Backend API:** http://176.222.53.185:8080
**Health Check:** http://176.222.53.185:8080/health
**GitHub:** https://github.com/RECTOR-LABS/asi-agents-track

---

**May Allah grant barakah and success in this demonstration! Bismillah!** 🚀
