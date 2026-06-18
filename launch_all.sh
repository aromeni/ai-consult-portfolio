#!/usr/bin/env bash
# Launch all 9 portfolio builds on separate ports.
# Usage: bash launch_all.sh
# Stop all: kill $(cat .launch_pids)

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$ROOT/.launch_pids"

if [ -f "$PID_FILE" ]; then
  echo "Stopping previous session..."
  while read -r pid; do kill "$pid" 2>/dev/null || true; done < "$PID_FILE"
  rm "$PID_FILE"
fi

declare -A BUILDS=(
  [8501]="brightpath-ai-readiness-tool"
  [8502]="document-intelligence-rag-demo"
  [8503]="semantic-rag-policy-assistant"
  [8504]="ai-staff-training-workshop-generator"
  [8505]="ai-consulting-report-generator"
  [8506]="ai-governance-policy-checker"
  [8507]="ai_adoption_roi_impact_tracker"
  [8508]="ai_adoption_delivery_tracker"
  [8509]="ai_adoption_consulting_capstone"
)

declare -A LABELS=(
  [8501]="Build 1 — AI Readiness + Workflow Audit Tool"
  [8502]="Build 2 — Document Intelligence / RAG Demo"
  [8503]="Build 3 — Semantic RAG Policy Assistant"
  [8504]="Build 4 — AI Staff Training + Workshop Generator"
  [8505]="Build 5 — AI Consulting Report Generator"
  [8506]="Build 6 — AI Governance Policy Checker"
  [8507]="Build 7 — AI Adoption ROI and Impact Tracker"
  [8508]="Build 8 — AI Adoption Delivery and Implementation Tracker"
  [8509]="Build 9 — AI Adoption Consulting Capstone Dashboard"
)

echo ""
echo "Starting portfolio builds..."
echo ""

for PORT in 8501 8502 8503 8504 8505 8506 8507 8508 8509; do
  DIR="$ROOT/builds/${BUILDS[$PORT]}"
  LABEL="${LABELS[$PORT]}"

  if [ ! -f "$DIR/app.py" ]; then
    echo "  SKIP  $LABEL (app.py not found at $DIR)"
    continue
  fi

  streamlit run "$DIR/app.py" \
    --server.port "$PORT" \
    --server.headless true \
    > "$ROOT/.build_${PORT}.log" 2>&1 &

  echo $! >> "$PID_FILE"
  echo "  PORT $PORT  $LABEL"
done

echo ""
echo "All builds launched. URLs:"
echo ""
for PORT in 8501 8502 8503 8504 8505 8506 8507 8508 8509; do
  echo "  http://localhost:$PORT  —  ${LABELS[$PORT]}"
done
echo ""
echo "Recommended entry point: http://localhost:8509 (Capstone Dashboard)"
echo ""
echo "To stop all:  kill \$(cat .launch_pids)"
echo "Logs:         .build_<port>.log"
