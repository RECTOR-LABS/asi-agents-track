# MediChain AI - Vercel Deployment Guide

## Overview

This guide walks through deploying the MediChain AI Next.js frontend to Vercel, connecting it to the VPS backend running on `176.222.53.185:8080`.

---

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) if you don't have one
2. **GitHub Repository**: Code already pushed to `RECTOR-LABS/asi-agents-track`
3. **VPS Backend Running**: Confirmed working at `http://176.222.53.185:8080`

---

## Deployment Steps

### 1. Import Project to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Select "Import Git Repository"
3. Choose your GitHub account (RECTOR-LABS)
4. Find and select `asi-agents-track` repository
5. Click "Import"

### 2. Configure Project Settings

**Framework Preset**: Next.js (auto-detected)

**Root Directory**:
```
medichain-web
```
⚠️ **IMPORTANT**: Set root directory to `medichain-web` since Next.js app is in a subdirectory

**Build Settings**:
- Build Command: `npm run build` (auto-detected)
- Output Directory: `.next` (auto-detected)
- Install Command: `npm install` (auto-detected)

### 3. Configure Environment Variables

Add the following environment variable:

| Key | Value | Description |
|-----|-------|-------------|
| `COORDINATOR_URL` | `http://176.222.53.185:8080` | VPS backend endpoint |

**How to add**:
1. Scroll to "Environment Variables" section
2. Click "Add Environment Variable"
3. Enter key: `COORDINATOR_URL`
4. Enter value: `http://176.222.53.185:8080`
5. Select "Production" environment
6. Click "Add"

### 4. Deploy

1. Click "Deploy" button
2. Wait for build to complete (~2-3 minutes)
3. Vercel will show deployment progress:
   - Installing dependencies
   - Building Next.js application
   - Deploying to edge network

### 5. Get Deployment URL

After deployment completes:
1. Vercel will show your deployment URL (e.g., `medichain-ai-xyz.vercel.app`)
2. Click the URL to open your deployed website
3. Copy this URL for testing

---

## Custom Domain (Optional)

If you want to use `medichain.rectorspace.com`:

### Add Custom Domain to Vercel

1. Go to your project settings
2. Navigate to "Domains" tab
3. Click "Add Domain"
4. Enter: `medichain.rectorspace.com`
5. Follow Vercel's DNS configuration instructions

### Configure DNS

Add these records to your DNS provider (where `rectorspace.com` is hosted):

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | medichain | cname.vercel-dns.com | 3600 |

Or if you want to use a subdomain:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | medichain | your-vercel-url.vercel.app | 3600 |

### Enable HTTPS

Vercel automatically provisions SSL certificates for custom domains.
- Certificate is issued within minutes
- Automatically renews
- Free Let's Encrypt certificate

---

## Testing Deployed Site

### 1. Health Check

Open your browser and test the landing page:
```
https://your-vercel-url.vercel.app/
```

You should see:
- MediChain AI landing page
- Features section
- Live demo chat interface at bottom

### 2. Test Diagnostic Flow

In the chat interface at the bottom of the page:

**Test Case 1 - Routine Condition**:
```
I have a severe headache and fever for 2 days
```

Expected response (10-15 seconds):
- Differential diagnoses: Influenza, COVID-19, Meningitis
- Urgency level: ROUTINE
- Treatment recommendations
- Specialist referral
- Medical disclaimer

**Test Case 2 - Emergency Condition**:
```
I have a sudden severe headache, stiff neck, confusion, and high fever
```

Expected response:
- Urgency level: EMERGENCY 🚨
- Red flags detected
- "Call 911 immediately" message
- Differential diagnosis: Meningitis

### 3. Browser Console

Open browser DevTools (F12) and check:
- No errors in Console
- Network tab shows successful API calls to VPS:
  ```
  POST http://176.222.53.185:8080/api/diagnose
  Status: 200 OK
  ```

---

## Troubleshooting

### Build Fails

**Error**: "Cannot find package.json"
- **Fix**: Ensure "Root Directory" is set to `medichain-web`

**Error**: "Module not found"
- **Fix**: Check `package.json` dependencies are correct
- Redeploy to trigger fresh install

### CORS Errors

**Error**: "Access-Control-Allow-Origin" error in browser
- **Fix**: VPS coordinator already configured for Vercel domains
- Check coordinator CORS settings include `https://*.vercel.app`

### API Timeout

**Error**: Request times out after 30 seconds
- **Check**: VPS backend is running
  ```bash
  curl http://176.222.53.185:8080/health
  ```
- **Check**: All 4 agent services are active
  ```bash
  ssh website 'sudo systemctl status medichain-*.service'
  ```

### Environment Variable Not Working

**Error**: API calls go to `localhost:8080` instead of VPS
- **Fix**: Verify `COORDINATOR_URL` is set in Vercel project settings
- **Fix**: Redeploy after adding environment variable

---

## Deployment Checklist

Before marking deployment complete:

- [ ] Project imported to Vercel
- [ ] Root directory set to `medichain-web`
- [ ] Environment variable `COORDINATOR_URL` configured
- [ ] Deployment successful (no build errors)
- [ ] Landing page loads correctly
- [ ] Chat interface visible
- [ ] Test Case 1 (routine) returns valid diagnosis
- [ ] Test Case 2 (emergency) returns urgent warning
- [ ] Browser console shows no errors
- [ ] VPS backend health check passes
- [ ] (Optional) Custom domain configured

---

## Post-Deployment

### Monitor VPS Resources

Check VPS resource usage:
```bash
ssh website 'htop'
```

Expected resource usage:
- 4 Python processes (agents)
- ~200-250MB total RAM
- Low CPU usage (<10% idle)

### Check Agent Logs

If issues occur, check agent logs:
```bash
# Coordinator logs
ssh website 'sudo journalctl -u medichain-coordinator.service -f'

# Patient Intake logs
ssh website 'sudo journalctl -u medichain-patient-intake.service -f'

# Symptom Analysis logs
ssh website 'sudo journalctl -u medichain-symptom-analysis.service -f'

# Treatment logs
ssh website 'sudo journalctl -u medichain-treatment.service -f'
```

### Restart Services (if needed)

```bash
# Restart all agents
ssh website 'sudo systemctl restart medichain-*.service'

# Check status
ssh website 'sudo systemctl status medichain-*.service'
```

---

## Success Criteria

✅ **Deployment Complete When**:
1. Vercel deployment shows "Ready" status
2. Landing page loads without errors
3. Chat interface accepts input
4. Diagnostic requests return valid responses within 30 seconds
5. Browser console shows no errors
6. VPS backend responds to health checks

---

## Demo Video Preparation

Once deployed, prepare for demo video recording:

1. **Clean Browser Session**: Use incognito mode
2. **Test Scenarios Ready**:
   - Routine condition (headache + fever)
   - Emergency condition (meningitis symptoms)
   - Edge case (vague symptoms)
3. **Screen Recording Tool**: OBS Studio, Loom, or macOS screen recording
4. **Script Prepared**: See `docs/DEMO-SCRIPT.md` (to be created)

---

## Next Steps

After Vercel deployment:
1. ✅ Phase 5.6: Deploy Next.js to Vercel
2. ⏳ Phase 5.7: Test production deployment end-to-end
3. ⏳ Phase 6: Update documentation and record demo video

---

**Need Help?**
- Vercel Docs: https://vercel.com/docs
- Next.js Deployment: https://nextjs.org/docs/deployment
- VPS Backend Logs: `ssh website 'sudo journalctl -u medichain-coordinator.service -f'`
