#!/usr/bin/env bash
# Launch all 9 portfolio builds on separate ports.
# Usage:    bash launch_all.sh
# Stop all: bash launch_all.sh stop

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$ROOT/.launch_pids"

# ── stop ────────────────────────────────────────────────────────────────────
if [ "${1:-}" = "stop" ]; then
  if [ -f "$PID_FILE" ]; then
    echo "Stopping all portfolio builds..."
    while read -r pid; do kill "$pid" 2>/dev/null || true; done < "$PID_FILE"
    rm "$PID_FILE"
    echo "Done."
  else
    echo "No running session found."
  fi
  exit 0
fi

# ── stop any previous session ────────────────────────────────────────────────
if [ -f "$PID_FILE" ]; then
  echo "Stopping previous session..."
  while read -r pid; do kill "$pid" 2>/dev/null || true; done < "$PID_FILE"
  rm "$PID_FILE"
fi

# ── helpers ──────────────────────────────────────────────────────────────────
launch() {
  local port="$1"
  local folder="$2"
  local label="$3"
  local dir="$ROOT/builds/$folder"

  if [ ! -f "$dir/app.py" ]; then
    echo "  SKIP  $label (not found)"
    return
  fi

  streamlit run "$dir/app.py" \
    --server.port "$port" \
    --server.headless true \
    > "$ROOT/.build_${port}.log" 2>&1 &

  echo $! >> "$PID_FILE"
  echo "  PORT $port  $label"
}

# ── launch ────────────────────────────────────────────────────────────────────
echo ""
echo "Starting Rashid AI Consult portfolio builds..."
echo ""

launch 8501 "brightpath-ai-readiness-tool"          "Build 1 — AI Readiness + Workflow Audit Tool"
launch 8502 "document-intelligence-rag-demo"         "Build 2 — Document Intelligence / RAG Demo"
launch 8503 "semantic-rag-policy-assistant"          "Build 3 — Semantic RAG Policy Assistant"
launch 8504 "ai-staff-training-workshop-generator"   "Build 4 — AI Staff Training + Workshop Generator"
launch 8505 "ai-consulting-report-generator"         "Build 5 — AI Consulting Report Generator"
launch 8506 "ai-governance-policy-checker"           "Build 6 — AI Governance Policy Checker"
launch 8507 "ai_adoption_roi_impact_tracker"         "Build 7 — AI Adoption ROI and Impact Tracker"
launch 8508 "ai_adoption_delivery_tracker"           "Build 8 — AI Adoption Delivery and Implementation Tracker"
launch 8509 "ai_adoption_consulting_capstone"        "Build 9 — AI Adoption Consulting Capstone Dashboard"

echo ""
echo "All builds launched. Open these URLs:"
echo ""
echo "  http://localhost:8501  —  Build 1 — AI Readiness + Workflow Audit Tool"
echo "  http://localhost:8502  —  Build 2 — Document Intelligence / RAG Demo"
echo "  http://localhost:8503  —  Build 3 — Semantic RAG Policy Assistant"
echo "  http://localhost:8504  —  Build 4 — AI Staff Training + Workshop Generator"
echo "  http://localhost:8505  —  Build 5 — AI Consulting Report Generator"
echo "  http://localhost:8506  —  Build 6 — AI Governance Policy Checker"
echo "  http://localhost:8507  —  Build 7 — AI Adoption ROI and Impact Tracker"
echo "  http://localhost:8508  —  Build 8 — AI Adoption Delivery and Implementation Tracker"
echo "  http://localhost:8509  —  Build 9 — AI Adoption Consulting Capstone Dashboard"
echo ""
echo "  Recommended entry point: http://localhost:8509"
echo ""
echo "  To stop all:  bash launch_all.sh stop"
echo "  Logs:         .build_<port>.log"
