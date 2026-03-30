#!/usr/bin/env bash
# ================================================================
#   CyberSentinel — Script de lancement global
#   Usage : bash start.sh
#   Ordre : 1. Shuffle  2. Labo Cyber  3. Flask
# ================================================================

set -euo pipefail

# ---- Couleurs ----
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_banner() {
    echo -e ""
    echo -e "${CYAN}${BOLD}  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     ${NC}"
    echo -e "${CYAN}${BOLD} ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ${NC}"
    echo -e "${CYAN}${BOLD} ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ${NC}"
    echo -e "${CYAN}${BOLD} ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ${NC}"
    echo -e "${CYAN}${BOLD} ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗${NC}"
    echo -e "${CYAN}${BOLD}  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝${NC}"
    echo -e "${DIM}                              Plateforme SaaS d'Audit de Sécurité Automatisé${NC}"
    echo -e ""
}

print_step() { echo -e "\n${CYAN}${BOLD}[$1/4]${NC} ${BOLD}$2${NC}"; }
print_ok()   { echo -e "      ${GREEN}✓${NC}  $1"; }
print_info() { echo -e "      ${YELLOW}→${NC}  $1"; }
print_err()  { echo -e "\n  ${RED}${BOLD}✗ ERREUR :${NC} $1\n"; }

# ---- Vérification Docker ----
if ! docker info &>/dev/null; then
    print_err "Docker n'est pas lancé. Démarrez Docker puis relancez ce script."
    exit 1
fi

print_banner

# ================================================================
# ÉTAPE 0 — Serveur de Wordlists (pour FFUF dans Shuffle)
# ================================================================
print_step 0 "Démarrage du serveur de Wordlists..."
WORDLIST_DIR="$ROOT_DIR/backend/Shuffle/shuffle-files"
pkill -f "python3 -m http.server 8888" 2>/dev/null || true
python3 -m http.server 8888 --directory "$WORDLIST_DIR" &>/dev/null &
echo $! > /tmp/wordlist-server.pid
print_ok "Serveur de wordlists démarré sur le port ${BOLD}8888${NC}"

# ================================================================
# ÉTAPE 1 — Shuffle (l'orchestrateur SOAR)
# ================================================================
print_step 1 "Démarrage de l'Orchestrateur Shuffle (SOAR)..."
print_info "Lancement des conteneurs Shuffle en arrière-plan..."

cd "$ROOT_DIR/backend/Shuffle"
docker compose up -d 2>&1 | while IFS= read -r line; do
    echo -e "      ${DIM}${line}${NC}"
done

print_ok "Conteneurs Shuffle lancés."
print_info "Attente de la disponibilité du service Shuffle (peut prendre ~60s)..."

TIMEOUT=120
ELAPSED=0
while ! curl -sk --max-time 3 "https://localhost:3443" -o /dev/null 2>/dev/null; do
    ELAPSED=$((ELAPSED + 3))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        print_err "Shuffle ne répond pas après ${TIMEOUT}s."
        echo -e "  ${YELLOW}Conseil :${NC} Vérifiez les logs avec :"
        echo -e "  ${DIM}docker compose -f backend/Shuffle/docker-compose.yml logs --tail=30${NC}\n"
        exit 1
    fi
    printf "\r      ${YELLOW}⏳${NC}  %ds / ${TIMEOUT}s — en attente de https://localhost:3443 ..." "$ELAPSED"
    sleep 3
done
printf "\r%-60s\n" ""   # efface la ligne de progression
print_ok "Shuffle opérationnel → ${BOLD}https://localhost:3443${NC}"

# ---- Mise à jour automatique de l'IP de callback dans le workflow ----
DOCKER_GW=$(docker network inspect shuffle_shuffle --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}' 2>/dev/null | head -1)
if [ -z "$DOCKER_GW" ]; then
    DOCKER_GW=$(hostname -I | awk '{print $1}')
fi
WORKFLOW_JSON="$ROOT_DIR/backend/audit_workflow.json"
sed -i "s|\"http://[0-9.]*:5000/api/report\"|\"http://${DOCKER_GW}:5000/api/report\"|g" "$WORKFLOW_JSON"
print_ok "Callback Flask mis à jour → ${BOLD}http://${DOCKER_GW}:5000/api/report${NC}"

# ================================================================
# ÉTAPE 2 — Laboratoire Cyber (site cible vulnérable + ZAP)
# ================================================================
print_step 2 "Démarrage du Laboratoire Cyber (cible + OWASP ZAP)..."
print_info "Connexion aux réseaux Shuffle (shuffle_shuffle, shuffle_swarm_executions)..."

cd "$ROOT_DIR/lab"
docker compose up -d 2>&1 | while IFS= read -r line; do
    echo -e "      ${DIM}${line}${NC}"
done

print_ok "Site cible vulnérable → ${BOLD}https://127.0.0.1:8443${NC}  (SSH: 127.0.0.1:2222)"
print_ok "OWASP ZAP prêt en arrière-plan."

# ================================================================
# ÉTAPE 3 — Flask (l'interface CyberSentinel)
# ================================================================
print_step 3 "Démarrage de l'Application Flask (CyberSentinel)..."

cd "$ROOT_DIR/frontend"

# Résumé final avant le démarrage
echo -e ""
echo -e "  ${GREEN}${BOLD}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "  ${GREEN}${BOLD}║       ✅  CyberSentinel est opérationnel !           ║${NC}"
echo -e "  ${GREEN}${BOLD}╠══════════════════════════════════════════════════════╣${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}  🌐  Interface Web     : ${BOLD}http://localhost:5000${NC}          ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}  🔧  Shuffle SOAR      : ${BOLD}https://localhost:3443${NC}         ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}  🎯  Labo Cyber (cible): ${BOLD}https://127.0.0.1:8443${NC}         ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}  🛡️   ZAP Proxy         : port ${BOLD}8080${NC} (interne)             ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}╠══════════════════════════════════════════════════════╣${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}  ${YELLOW}Ctrl+C${NC} pour tout arrêter proprement.                ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}╚══════════════════════════════════════════════════════╝${NC}"
echo -e ""
echo -e "  ${DIM}Logs Flask ci-dessous ↓${NC}"
echo -e ""

# ---- Nettoyage propre sur Ctrl+C ----
cleanup() {
    echo -e "\n\n  ${YELLOW}${BOLD}Arrêt de CyberSentinel en cours...${NC}"

    echo -e "  ${DIM}→ Arrêt du serveur de wordlists...${NC}"
    if [ -f /tmp/wordlist-server.pid ]; then
        kill "$(cat /tmp/wordlist-server.pid)" 2>/dev/null || true
        rm -f /tmp/wordlist-server.pid
    fi

    echo -e "  ${DIM}→ Arrêt du Laboratoire Cyber...${NC}"
    cd "$ROOT_DIR/lab" && docker compose down --remove-orphans 2>/dev/null || true

    echo -e "  ${DIM}→ Arrêt de Shuffle...${NC}"
    cd "$ROOT_DIR/backend/Shuffle" && docker compose down --remove-orphans 2>/dev/null || true

    echo -e "  ${GREEN}✓  Tout est arrêté proprement.${NC}\n"
    exit 0
}
trap cleanup INT TERM

# Démarrage de Flask au premier plan (logs visibles directement)
python3 app.py
