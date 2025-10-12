# MediChain AI - Video Demo Guide (3-5 Minutes)

**Quick Reference for Recording Hackathon Demo Video**

---

## 📹 Recording Setup (2 minutes)

### Tools
- **Screen Recorder**: OBS Studio, Loom, or macOS QuickTime (Cmd+Shift+5)
- **Resolution**: 1920x1080
- **Audio**: Test microphone before starting
- **Browser**: Chrome/Edge (clean, no personal bookmarks visible)

### Before Recording
1. Close unnecessary tabs
2. Clear browser cache
3. Test both URLs:
   - Pitch site: https://medichain-web.rectorspace.com (landing page)
   - Agentverse: https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q
4. Prepare 2 test inputs (copy to clipboard):
   - Emergency: `Severe headache, high fever, stiff neck - started 6 hours ago, age 28`
   - Routine: `I have a severe headache and fever for 2 days`
5. Practice once (optional but recommended)

---

## 🎬 Video Script (3-5 Minutes)

### [0:00-0:40] Opening (40 seconds)

**Show: Landing page of MediChain AI**

**Say:**
> "Healthcare diagnostics are expensive and often inaccessible. Patients wait hours for triage, and AI diagnostic tools lack transparency in their reasoning.
>
> MediChain AI solves this with a multi-agent system powered by Fetch.ai's uAgents framework and SingularityNET's MeTTa knowledge graph.
>
> Four specialized agents work together to provide transparent, evidence-based medical diagnostics in seconds."

**Action:** Scroll slowly through landing page

---

### [0:40-1:30] Architecture (50 seconds)

**Show: Architecture diagram on landing page**

**Say:**
> "The system uses 4 specialized agents:
> - Patient Intake extracts symptoms using NLP
> - Symptom Analysis performs triage and detects red flags
> - Treatment Recommendation suggests evidence-based treatments with safety checks
> - Coordinator orchestrates everything
>
> All agents query a MeTTa knowledge graph with 200+ medical facts, 13 conditions, and contraindication checking.
>
> This deep integration with MeTTa enables transparent reasoning - you see confidence scores, differential diagnoses, and evidence sources."

**Action:** Point to each agent in diagram

---

### [1:30-3:30] Live Demo - Emergency Case (2 minutes) ⭐ **MOST IMPORTANT**

**Show: Navigate to Agentverse agent page**

**Say:**
> "Let me show you a live example via Agentverse - the official Fetch.ai platform. Here's an emergency case - symptoms of possible meningitis."

**Action:**
1. Visit: https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q
2. Click "Chat with Agent" button
3. In chat interface, paste:
   ```
   Severe headache, high fever, stiff neck - started 6 hours ago, age 28
   ```
4. **While waiting (10-15 seconds):**
   > "The agents are now communicating through the ASI ecosystem. Patient Intake extracts symptoms, Symptom Analysis queries the MeTTa knowledge base for matching conditions, and evaluates urgency..."

5. **When response appears:**
   > "The system correctly identified this as EMERGENCY.
   >
   > It detected the meningitis triad - red flags that require immediate attention.
   >
   > The differential diagnosis shows Meningitis with confidence scores.
   >
   > And most importantly - it says 'Call 911 immediately' with time-sensitive warnings.
   >
   > This is MeTTa reasoning in action - transparent, explainable AI running on the official Fetch.ai infrastructure."

**Action:** Slowly scroll through response, highlighting:
- Emergency classification
- Red flags detected
- Differential diagnoses with confidence
- Treatment recommendations
- Emergency action message

---

### [3:30-4:30] Live Demo - Routine Case (1 minute)

**Say:**
> "Now let's contrast with a routine case in the same Agentverse chat."

**Action:**
1. In the same chat session, paste: `I have a severe headache and fever for 2 days`
2. Send

**While waiting:**
> "Same multi-agent process, but the MeTTa knowledge graph will classify this differently..."

**When response appears:**
> "This time we see ROUTINE classification.
>
> Differential diagnoses include Influenza and COVID-19 with confidence scores around 15-20%.
>
> Treatment recommendations are conservative: antivirals, rest, fluids.
>
> Referral to primary care, not emergency.
>
> The system adapts based on urgency - this is intelligent triage running on the official ASI infrastructure."

**Action:** Scroll through response

---

### [4:30-5:00] Closing (30 seconds)

**Show: Return to top of page or architecture**

**Say:**
> "MediChain AI demonstrates the power of multi-agent systems with deep MeTTa integration - deployed on the official ASI ecosystem.
>
> It's production-ready, running 24/7 on VPS with mailbox connections to Agentverse.
>
> The transparent reasoning, safety checks, and evidence-based approach make it suitable for real-world healthcare triage.
>
> This is the future of explainable AI in healthcare - decentralized, transparent, and accessible through the ASI Alliance infrastructure."

**Action:** Return to landing page or agent profile

**End screen text (optional):**
```
MediChain AI
Decentralized Healthcare Diagnostics

🔗 medichain-web.rectorspace.com (Pitch Site)
🤖 Test on Agentverse (Live Demo)
🐙 github.com/RECTOR-LABS/asi-agents-track

Built for ASI Agents Track Hackathon 2025
```

---

## ✅ Post-Recording Checklist

- [ ] Watch full video (check audio, visuals)
- [ ] Verify both demo cases shown clearly
- [ ] Trim any mistakes/long pauses
- [ ] Add title card (optional: first 3 seconds)
- [ ] Export as MP4 (1920x1080, 30fps)
- [ ] Upload to YouTube
- [ ] Set as **Unlisted** or **Public**
- [ ] Copy video URL
- [ ] Add to README.md

---

## 🎯 Key Messages to Emphasize

1. **Multi-agent architecture** (4 specialized agents)
2. **Deep MeTTa integration** (200+ facts, not superficial)
3. **Transparent reasoning** (confidence scores, differential diagnoses)
4. **Production-ready** (deployed, working 24/7)
5. **Safety-first** (emergency detection, contraindications)
6. **Evidence-based** (CDC, WHO, medical guidelines)

---

## 💡 Pro Tips

- **Start with emergency case** - Most visually impressive (RED badge)
- **Speak confidently** - You built something amazing!
- **Show, don't just tell** - Let the demo speak for itself
- **Emphasize MeTTa** - Judges care about deep integration
- **Keep cursor movements smooth** - Avoid jerky scrolling
- **Smile** (if showing face) - Enthusiasm is contagious!

---

## 🚨 If Something Goes Wrong During Recording

**Backend timeout:**
- Pause recording
- Check health: `curl http://176.222.53.185:8080/health`
- Restart services: `ssh website 'sudo systemctl restart medichain-*.service'`
- Wait 10 seconds, resume recording

**Frontend error:**
- Refresh page (Cmd/Ctrl + Shift + R)
- Try incognito mode
- Worst case: Show screenshots/screen recording from earlier test

**Keep calm and confident!** Minor glitches happen - acknowledge and continue.

---

## 📤 After Video is Done

**Upload Checklist:**
1. Upload to YouTube
2. Title: "MediChain AI - Decentralized Healthcare Diagnostics (ASI Agents Track 2025)"
3. Description:
   ```
   MediChain AI is a multi-agent diagnostic system built for the ASI Agents Track Hackathon 2025.

   🔗 Live Demo: https://medichain-web.rectorspace.com
   🐙 GitHub: https://github.com/RECTOR-LABS/asi-agents-track

   Built with:
   - Fetch.ai uAgents Framework (multi-agent communication)
   - SingularityNET MeTTa (knowledge graph reasoning)
   - 4 specialized agents (Coordinator, Patient Intake, Symptom Analysis, Treatment)
   - 200+ medical facts, 13 conditions
   - Transparent, evidence-based diagnostics

   #AIHackathon #ASIAlliance #FetchAI #SingularityNET #MeTTa #Healthcare #MultiAgent
   ```
4. Thumbnail: Screenshot of emergency case (RED badge)
5. Playlist: Create "ASI Agents Track 2025" playlist
6. Copy video URL
7. Update README.md with link

---

**Bismillah! You've got this! 🚀**

**Total Recording Time: 5 minutes**
**Total Prep Time: 10 minutes**
**Total Process: 15-20 minutes to completion**
