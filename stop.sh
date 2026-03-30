#!/usr/bin/env bash
# ================================================================
#   CyberSentinel — Script d'arrêt global
#   Usage : bash stop.sh
# ================================================================

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; DIM='\033[2m'; BOLD='\033[1m'; NC='\033[0m'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "\n  ${YELLOW}${BOLD}Arrêt de CyberSentinel...${NC}\n"

echo -e "  ${DIM}→ Arrêt du serveur de wordlists...${NC}"
if [ -f /tmp/wordlist-server.pid ]; then
    kill "$(cat /tmp/wordlist-server.pid)" 2>/dev/null || true
    rm -f /tmp/wordlist-server.pid
fi
pkill -f "python3 -m http.server 8888" 2>/dev/null || true

echo -e "  ${DIM}→ Arrêt du Laboratoire Cyber...${NC}"
cd "$ROOT_DIR/lab"
docker compose down --remove-orphans 2>&1 | grep -v "^$" | while IFS= read -r line; do
    echo -e "     ${DIM}${line}${NC}"
done

echo -e "  ${DIM}→ Arrêt de Shuffle (SOAR)...${NC}"
cd "$ROOT_DIR/backend/Shuffle"
docker compose down --remove-orphans 2>&1 | grep -v "^$" | while IFS= read -r line; do
    echo -e "     ${DIM}${line}${NC}"
done

echo -e "\n  ${GREEN}${BOLD}✓  CyberSentinel est arrêté.${NC}\n"
