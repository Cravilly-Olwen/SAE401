<div align="center">

```
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
```

### 🛡️ Plateforme d'Audit de Sécurité Web Automatisé

*Le contrôle technique de votre site internet*

---

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Required-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Shuffle](https://img.shields.io/badge/Shuffle-SOAR-FF6B35?style=for-the-badge)
![OWASP](https://img.shields.io/badge/OWASP_ZAP-Intégré-000000?style=for-the-badge&logo=owasp&logoColor=white)
![License](https://img.shields.io/badge/Mode-White_Hat_✓-00B894?style=for-the-badge)

</div>

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
  - [1 · Cloner le projet](#1--cloner-le-projet)
  - [2 · Installer Docker](#2--installer-docker)
  - [3 · Lancer Shuffle](#3--lancer-shuffle-orchestrateur)
  - [4 · Importer le workflow](#4--importer-le-workflow-daudit)
  - [5 · Démarrer le lab vulnérable](#5--démarrer-le-site-vulnérable-lab)
  - [6 · Configurer Flask](#6--installer-et-configurer-flask)
  - [7 · Démarrer CyberSentinel](#7--démarrer-cybersentinel)
- [Utilisation](#-utilisation)
- [Scoring ANSSI](#-scoring-anssi)
- [Dépannage](#-dépannage)

---

## 🔍 Vue d'ensemble

**CyberSentinel** orchestre 6 outils de sécurité open-source en parallèle et traduit leurs résultats bruts en un **rapport vulgarisé**, inspiré du modèle WooRank pour le SEO.

```
┌─────────────────────────────────────────────────────────────────┐
│                      CYBERSENTINEL                              │
│                                                                 │
│   [Utilisateur]  ──►  [Flask :5000]  ──►  [Shuffle SOAR]       │
│                             │                    │              │
│                             │         ┌──────────▼──────────┐  │
│                             │         │  dig   │   nmap      │  │
│                             │         │  nikto │   ffuf      │  │
│                             │         │ testssl│  OWASP ZAP  │  │
│                             │         └──────────┬──────────┘  │
│                             │                    │              │
│                    [Dashboard]  ◄──  [Parseur ANSSI Python]     │
│                    [PDF / Email]                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Architecture

```
SAE401/
│
├── 📁 frontend_flask/              → Interface web & API
│   ├── app.py                      → Serveur Flask principal
│   ├── templates/
│   │   ├── index.html              → Formulaire d'audit
│   │   ├── dashboard.html          → Tableau de bord résultats
│   │   └── report_pdf.html         → Template rapport PDF
│   └── static/
│       ├── css/                    → Styles
│       └── js/                     → Scripts frontend
│
├── 📁 backend_orchestrator/        → Moteur SOAR
│   └── Moteur_Audit_SAE401.json    → Workflow Shuffle (à importer)
│
└── 📁 dummy_site/                  → Laboratoire de test
    ├── app.py                      → Site Flask avec failles intentionnelles
    ├── Dockerfile
    ├── docker-compose.yml
    └── requirements.txt
```

---

## ✅ Prérequis

| Composant | Version minimale | Vérification |
|---|---|---|
| OS | Ubuntu 22.04 / Debian 12 / WSL2 | `uname -a` |
| Python | 3.10+ | `python3 --version` |
| Docker | 24.0+ | `docker --version` |
| Docker Compose | v2.0+ | `docker compose version` |
| RAM disponible | 4 Go (8 Go recommandés) | `free -h` |
| Ports libres | 3443, 5000, 8080, 8443, 2222 | `ss -tlnp` |

---

## 🚀 Installation

### 1 · Cloner le projet

```bash
git clone https://github.com/Cravilly-Olwen/SAE401.git
cd SAE401
git checkout Jeremy
```

---

### 2 · Installer Docker

> ⏭️ **Passez cette étape si Docker est déjà installé.**

```bash
# Téléchargement et installation automatique
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter votre utilisateur au groupe docker (évite sudo à chaque fois)
sudo usermod -aG docker $USER
newgrp docker

# Vérification
docker --version
docker compose version
```

---

### 3 · Lancer Shuffle (Orchestrateur)

Shuffle est le **cerveau** de la plateforme. Il exécute et parallélise tous les outils d'audit.

```bash
# Cloner Shuffle dans /opt
git clone https://github.com/Shuffle/Shuffle.git /opt/shuffle
cd /opt/shuffle

# Démarrer tous les conteneurs Shuffle
docker compose up -d

# Attendre que les services soient prêts (~60 secondes)
echo "Attente du démarrage de Shuffle..."
sleep 60
docker ps | grep shuffle
```

> 🌐 **Interface Shuffle :** [`https://localhost:3443`](https://localhost:3443)
>
> ⚠️ Ignorez l'avertissement SSL (certificat auto-signé) et créez un compte administrateur à la première connexion.

**Vérifier que les réseaux Docker Shuffle existent :**

```bash
docker network ls | grep shuffle
```

Vous devez voir **deux lignes** :
```
shuffle_shuffle
shuffle_swarm_executions
```

S'ils sont absents, créez-les manuellement :

```bash
docker network create shuffle_shuffle
docker network create shuffle_swarm_executions
```

---

### 4 · Importer le workflow d'audit

1. Connectez-vous sur [`https://localhost:3443`](https://localhost:3443)
2. Allez dans **Workflows** dans le menu
3. Cliquez sur le bouton **Import** (icône ☁️)
4. Sélectionnez le fichier :

```
backend_orchestrator/Moteur_Audit_SAE401.json
```

5. Le workflow **Moteur_Audit_SAE401** apparaît dans votre liste ✅

#### 📌 Récupérer l'URL du Webhook

Ouvrez le workflow et cliquez sur le bloc **`Reception_Commande_Flask`** (trigger Webhook).

Copiez l'URL affichée, elle ressemble à :

```
https://127.0.0.1:3443/api/v1/hooks/webhook_b8ae0f49-ef46-487e-bbd8-b6674650e17b
```

> 🔑 **Gardez cette URL** — vous en aurez besoin à l'étape 6.

#### 📌 Mettre à jour l'IP Flask dans Shuffle

Dans le workflow, ouvrez le bloc **`Envoi_Flask`** et mettez à jour l'URL avec l'IP réelle de votre machine :

```
http://VOTRE_IP_LOCALE:5000/api/report
```

Pour trouver votre IP locale :

```bash
ip a | grep "inet " | grep -v 127.0.0.1
# Exemple de résultat : inet 192.168.1.42/24
```

---

### 5 · Démarrer le site vulnérable (lab)

Ce site simule une cible réelle avec des **failles intentionnelles** pour tester la plateforme.

| Faille | Description | Outil détecteur |
|---|---|---|
| Header `Server: Apache/2.2.14` | Version obsolète exposée | Nikto |
| Fichier `/config.bak` public | Fuite de credentials BDD | FFUF |
| `/robots.txt` révèle des dossiers | Information disclosure | Nikto |
| Certificat SSL auto-signé | TLS invalide | TestSSL |
| Port SSH 22 ouvert | Service sensible exposé | Nmap |
| Paramètre `?q=` non échappé | XSS potentiel | OWASP ZAP |

```bash
cd dummy_site

# Construire et démarrer
docker compose up -d --build

# Vérifier que les conteneurs tournent
docker ps
```

Services disponibles après démarrage :

| Service | Accès | Détail |
|---|---|---|
| Site HTTPS vulnérable | `https://127.0.0.1:8443` | Cible principale des tests |
| OWASP ZAP | `http://127.0.0.1:8080` | Scanner applicatif automatique |
| SSH exposé | `ssh root@127.0.0.1 -p 2222` | Mot de passe : `cyber2026` |

Tester l'accès au lab :

```bash
curl -k https://127.0.0.1:8443
```

---

### 6 · Installer et configurer Flask

#### 6.1 — Dépendances système

WeasyPrint (génération PDF) nécessite des bibliothèques système spécifiques :

```bash
sudo apt update && sudo apt install -y \
    python3 python3-pip python3-venv \
    libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    libcairo2 libgtk-3-0
```

#### 6.2 — Environnement virtuel Python

```bash
cd frontend_flask

python3 -m venv venv
source venv/bin/activate
# Windows : venv\Scripts\activate
```

#### 6.3 — Dépendances Python

```bash
pip install flask==3.0.0 werkzeug==3.0.0 weasyprint requests urllib3
```

#### 6.4 — Configurer l'URL du webhook Shuffle

Ouvrez `frontend_flask/app.py` et remplacez la ligne ~47 avec votre URL du webhook (copiée à l'étape 4) :

```python
shuffle_webhook_url = "https://127.0.0.1:3443/api/v1/hooks/webhook_VOTRE_ID_ICI"
```

#### 6.5 — (Optionnel) Activer l'envoi d'email

Dans `frontend_flask/app.py`, modifiez les lignes ~130 :

```python
SENDER_EMAIL    = "votre.email@gmail.com"
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"   # Mot de passe d'application Gmail
```

<details>
<summary>💡 Comment créer un mot de passe d'application Gmail ?</summary>

1. Allez sur **myaccount.google.com**
2. **Sécurité** → Validation en 2 étapes (à activer si nécessaire)
3. **Sécurité** → Mots de passe des applications
4. Choisissez "Autre" → nommez-le `CyberSentinel`
5. Copiez le mot de passe généré (format : `xxxx xxxx xxxx xxxx`)

</details>

---

### 7 · Démarrer CyberSentinel

```bash
cd frontend_flask
source venv/bin/activate
python app.py
```

Sortie attendue :

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

> 🌐 **CyberSentinel est disponible sur :** [`http://localhost:5000`](http://localhost:5000)

---

## 🎯 Utilisation

### Lancer un audit

```
1. Ouvrir      →  http://localhost:5000
2. URL cible   →  ex: https://127.0.0.1:8443
3. Mode        →  Simple  ou  Avancé
4. Cliquer     →  [ Lancer l'audit ]
5. Patienter   →  la page se rafraîchit automatiquement
6. Consulter   →  le dashboard avec scoring et vulnérabilités détaillées
```

### Modes d'audit

| Mode | Outils actifs | Durée estimée |
|---|---|---|
| **Simple** | `dig` + `nmap` + `nikto` | ~2 min |
| **Avancé** | Simple + `ffuf` + `testssl` + `OWASP ZAP` | ~8 min |

### Exporter le rapport

| Action | Description |
|---|---|
| 📥 **Télécharger PDF** | Rapport complet et détaillé au format PDF |
| 📧 **Envoyer par email** | Envoi du PDF à l'adresse saisie |

---

## 📊 Scoring ANSSI

Le scoring est calculé selon la **matrice Impact × Difficulté d'exploitation** de l'ANSSI :

```
                   Difficulté d'exploitation →
                ┌──────────┬──────────┬──────────┬──────────┐
                │Très diff.│ Difficile│ Modérée  │  Facile  │
  ┌─────────────┼──────────┼──────────┼──────────┼──────────┤
  │   Mineur    │  Mineur  │  Mineur  │Important │  Majeur  │
↓ ├─────────────┼──────────┼──────────┼──────────┼──────────┤
I │   Important │  Mineur  │Important │Important │  Majeur  │
m ├─────────────┼──────────┼──────────┼──────────┼──────────┤
p │   Majeur    │Important │  Majeur  │  Majeur  │ CRITIQUE │
a ├─────────────┼──────────┼──────────┼──────────┼──────────┤
c │   Critique  │Important │  Majeur  │ CRITIQUE │ CRITIQUE │
t └─────────────┴──────────┴──────────┴──────────┴──────────┘
```

### Calcul du score global

```
Score = 100 − (Critique × 25) − (Majeur × 15) − (Important × 5) − (Mineur × 1)
```

| Grade | Score | Signification |
|---|---|---|
| 🟢 **A** | ≥ 90 | Excellent — Situation saine |
| 🔵 **B** | ≥ 70 | Bon — Ajustements recommandés |
| 🟡 **C** | ≥ 50 | Moyen — Faiblesses importantes |
| 🟠 **D** | ≥ 20 | Dangereux — Intervention rapide requise |
| 🔴 **F** | < 20 | Critique — Urgence absolue |

---

## 🔧 Dépannage

<details>
<summary>❌ Le dashboard n'apparaît jamais après l'audit</summary>

Cause probable : Shuffle ne peut pas envoyer le rapport à Flask.

```bash
# 1. Vérifier que Shuffle tourne
docker ps | grep shuffle

# 2. Vérifier les réseaux Docker
docker network ls | grep shuffle

# 3. Tester le webhook manuellement
curl -k -X POST https://127.0.0.1:3443/api/v1/hooks/VOTRE_WEBHOOK_ID \
  -H "Content-Type: application/json" \
  -d '{"clean_target":"test.com","full_url":"https://test.com","mode":"simple"}'
```

Vérifiez que l'IP dans le bloc `Envoi_Flask` du workflow Shuffle est bien celle de votre machine (pas `localhost` ni `127.0.0.1`).

</details>

<details>
<summary>❌ Erreur WeasyPrint / génération PDF échoue</summary>

```bash
# Réinstaller les dépendances système
sudo apt install -y --reinstall \
    libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2

# Tester WeasyPrint
python3 -c "import weasyprint; print('WeasyPrint OK')"
```

</details>

<details>
<summary>❌ Le dummy site n'est pas accessible sur le port 8443</summary>

```bash
cd dummy_site

# Voir les logs
docker compose logs laboratoire_cyber

# Reconstruire et redémarrer
docker compose down && docker compose up -d --build

# Tester
curl -k https://127.0.0.1:8443
```

</details>

<details>
<summary>❌ OWASP ZAP ne retourne pas de résultats</summary>

ZAP peut être lent à initialiser. Attendez 30 secondes après le `docker compose up`, puis :

```bash
# Vérifier que ZAP répond
curl "http://localhost:8080/JSON/core/view/version/?apikey=12345"
# Attendu : {"version":"2.x.x"}

# Si ZAP ne répond pas
docker restart zap-server
```

</details>

<details>
<summary>❌ Erreur "Port already in use"</summary>

```bash
# Identifier quel processus utilise le port (ex: 5000)
sudo lsof -i :5000
sudo lsof -i :3443
sudo lsof -i :8080
sudo lsof -i :8443

# Tuer le processus bloquant
sudo kill -9 <PID>
```

</details>

---

## 🔒 Charte éthique — Mode White Hat

> ⚠️ **CyberSentinel est un outil d'audit défensif uniquement.**

- ✅ Aucune exploitation — observation passive uniquement
- ✅ Temporisation intégrée dans tous les scans (pas de DDoS involontaire)
- ✅ 100% open-source, aucune dépendance propriétaire
- ❌ **N'utilisez jamais cet outil sur une cible sans autorisation écrite explicite**

L'utilisation de CyberSentinel sur des systèmes tiers sans permission est illégale (Code pénal français, Art. 323-1).

---

## 👥 Équipe

Projet **SAE 401** — BUT Informatique 2025/2026

> Encadrant : **Christian Delettre**, PhD
> Fondateur & CEO de `</DelTekZen>` — Expert en transformation digitale

---

<div align="center">

*Made with ❤️ and way too much caffeine ☕*

</div>
