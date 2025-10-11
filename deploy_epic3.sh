#!/bin/bash
# Epic 3 Deployment Script - MediChain AI
# Deploys Symptom Analysis and Treatment Recommendation Agents

echo "═══════════════════════════════════════════════════════════"
echo "🚀 EPIC 3 DEPLOYMENT - MEDICHAIN AI"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Please copy .env.example to .env and configure it"
    exit 1
fi

# Source environment
source venv/bin/activate

echo "📋 Deployment Checklist:"
echo ""
echo "BEFORE RUNNING THIS SCRIPT:"
echo "  1. Ensure all existing agents are stopped"
echo "  2. Update .env with existing agent addresses"
echo "  3. Have Agentverse Inspector ready in browser"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Function to deploy an agent
deploy_agent() {
    local AGENT_NAME=$1
    local AGENT_FILE=$2
    local AGENT_PORT=$3
    local LOG_FILE=$4

    echo "─────────────────────────────────────────────────────────"
    echo "📦 Deploying: $AGENT_NAME"
    echo "─────────────────────────────────────────────────────────"
    echo "   Port: $AGENT_PORT"
    echo "   Log: $LOG_FILE"
    echo ""

    # Start agent in background
    echo "   🔄 Starting agent..."
    python $AGENT_FILE > $LOG_FILE 2>&1 &
    local PID=$!

    echo "   ✅ Agent started (PID: $PID)"
    echo "   📝 Monitor logs: tail -f $LOG_FILE"
    echo ""

    # Wait for agent to start
    sleep 5

    # Extract inspector URL from logs
    INSPECTOR_URL=$(grep -m 1 "Agent inspector available" $LOG_FILE | sed 's/.*https/https/')

    if [ ! -z "$INSPECTOR_URL" ]; then
        echo "   🔗 INSPECTOR URL:"
        echo "   $INSPECTOR_URL"
        echo ""
        echo "   📌 NEXT STEPS:"
        echo "   1. Copy the URL above"
        echo "   2. Open in browser"
        echo "   3. Click 'Connect' button (top right)"
        echo "   4. Select 'Mailbox' option"
        echo "   5. Click 'OK, got it'"
        echo "   6. Wait for mailbox registration confirmation in logs"
        echo "   7. Copy agent address from logs"
        echo "   8. Update .env file with agent address"
        echo ""
    else
        echo "   ⚠️  Could not extract inspector URL from logs"
        echo "   Check logs manually: $LOG_FILE"
        echo ""
    fi

    # Wait for user confirmation
    read -p "   Press ENTER once mailbox is created and agent address is copied..."
    echo ""

    # Extract agent address from logs
    AGENT_ADDRESS=$(grep -m 1 "Agent Address:" $LOG_FILE | awk '{print $NF}')

    if [ ! -z "$AGENT_ADDRESS" ]; then
        echo "   📍 Agent Address: $AGENT_ADDRESS"
        echo "   💡 Add this to .env file:"
        echo ""
        echo "   ${AGENT_NAME}_ADDRESS=$AGENT_ADDRESS"
        echo ""
    fi

    echo "   ✅ $AGENT_NAME deployment complete!"
    echo "─────────────────────────────────────────────────────────"
    echo ""
}

# Deploy Symptom Analysis Agent
deploy_agent \
    "SYMPTOM_ANALYSIS" \
    "src/agents/symptom_analysis.py" \
    "8004" \
    "/tmp/symptom_analysis_deploy.log"

# Deploy Treatment Recommendation Agent
deploy_agent \
    "TREATMENT_RECOMMENDATION" \
    "src/agents/treatment_recommendation.py" \
    "8005" \
    "/tmp/treatment_recommendation_deploy.log"

echo "═══════════════════════════════════════════════════════════"
echo "✅ EPIC 3 DEPLOYMENT COMPLETE!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📊 DEPLOYMENT SUMMARY:"
echo "   Symptom Analysis Agent: Port 8004"
echo "   Treatment Recommendation Agent: Port 8005"
echo ""
echo "📝 FINAL STEPS:"
echo "   1. Verify both agent addresses are in .env"
echo "   2. Restart coordinator agent to pick up new addresses"
echo "   3. Test end-to-end flow via Agentverse chat"
echo ""
echo "🔍 VERIFY DEPLOYMENT:"
echo "   - Visit https://agentverse.ai/agents"
echo "   - Check both agents show 'Active' status"
echo "   - Check both agents have 'Mailbox' badge"
echo ""
echo "🧪 TEST FLOW:"
echo "   User → Coordinator → Patient Intake → Symptom Analysis → Treatment Recommendation → User"
echo ""
echo "═══════════════════════════════════════════════════════════"
