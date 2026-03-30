# CyberSentinel — Plateforme d'Audit de Cybersécurité Automatisée

> **SAE 401** — BUT Réseaux & Télécommunications | Année 2025–2026
> Plateforme SaaS d'audit de sécurité à 360°, orchestrée par SOAR, avec tableau de bord vulgarisé basé sur la métaphore du **Contrôle Technique Automobile**.

---

## Table des matières

1. [Présentation du projet](#1-présentation-du-projet)
2. [Fonctionnalités](#2-fonctionnalités)
3. [Stack technique](#3-stack-technique)
4. [Architecture du dépôt](#4-architecture-du-dépôt)
5. [Structure détaillée des fichiers](#5-structure-détaillée-des-fichiers)
6. [Installation et lancement](#6-installation-et-lancement)
7. [Système de scoring ANSSI](#7-système-de-scoring-anssi)
8. [Environnement de test](#8-environnement-de-test)
9. [Documentation et livrables](#9-documentation-et-livrables)

---

## 1. Présentation du projet

**CyberSentinel** est une application SaaS qui démocratise la cybersécurité pour les non-experts. Elle orchestre en arrière-plan six outils d'audit professionnels et restitue les résultats sous la forme d'un tableau de bord vulgarisé, inspiré du **Contrôle Technique Automobile** et des rapports SEO type WooRank.

L'objectif est de permettre à n'importe quelle organisation, sans compétences techniques avancées, d'obtenir une vue claire et priorisée de sa posture de sécurité en quelques clics.

**Deux modes d'exécution :**
- **Mode Simple** — Scan rapide de surface (Reconnaissance DNS, ports, TLS).
- **Mode Avancé** — Analyse profonde avec fuzzing web et DAST (détection de SQLi, XSS, etc.).

---

## 2. Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Audit 360° | Analyse du domaine, de l'hébergement serveur et de la couche applicative web |
| Double mode | Mode Simple (surface) et Mode Avancé (fuzzing + DAST) |
| Tableau de bord vulgarisé | Résultats traduits en langage clair via la métaphore automobile (ANSSI) |
| Rapport PDF | Génération automatique d'un rapport complet au format PDF |
| Envoi par e-mail | Distribution du rapport PDF directement par e-mail SMTP |
| Surveillance continue | Abonnement à un audit quotidien automatisé (cron à 8h00) |
| Alerte sur nouvelle faille | Notification par mail si une nouvelle vulnérabilité est détectée |
| Éthique White Hat | Temporisation des requêtes intégrée (anti-DDoS involontaire) |
| Environnement de test | Site vulnérable local pour valider chaque outil d'audit |

---

## 3. Stack technique

### Frontend
| Technologie | Rôle |
|---|---|
| Python 3 + Flask | Serveur web, routing, logique métier |
| Jinja2 | Moteur de templates HTML |
| HTML / CSS / JavaScript | Interface utilisateur |
| WeasyPrint / pdfkit | Génération de rapports PDF |
| APScheduler | Planification des audits automatiques (cron) |
| smtplib | Envoi des rapports par e-mail |

### Backend / Orchestration
| Technologie | Rôle |
|---|---|
| Shuffle (SOAR) | Orchestrateur de workflows d'audit |
| Go (Golang) | Moteur backend de Shuffle |
| OpenSearch | Base de données des résultats et logs |
| React.js | Interface d'administration Shuffle |
| Docker / Docker Compose | Conteneurisation de tous les services |

### Outils d'audit intégrés (6)
| Outil | Catégorie | Fonction |
|---|---|---|
| `dig` | Reconnaissance | Analyse DNS, zone transfer, MX, NS |
| `Nmap` | Reconnaissance | Scan de ports, détection de services et OS |
| `testssl.sh` | Cryptographie | Analyse TLS/HTTPS, certificats, chiffrements |
| `Nikto` | Configuration serveur | Fichiers dangereux, headers manquants, versions exposées |
| `FFUF` | Fuzzing web | Découverte de répertoires et fichiers cachés |
| `OWASP ZAP` | DAST | Détection active de SQLi, XSS, CSRF et autres failles applicatives |

---

## 4. Architecture du dépôt

```
SAE401/
│
├── frontend_flask/          # Interface web Flask (port 5000)
├── backend_orchestrator/    # Moteur d'audit Shuffle SOAR (port 3443)
├── dummy_site/              # Site web vulnérable pour les tests (port 8443)
├── docs/                    # Documentation technique du projet
│
├── start.sh                 # Script de démarrage global (tous les services)
├── stop.sh                  # Script d'arrêt global
├── README.md                # Ce fichier
│
├── SAE401.pdf                               # Cahier des charges SAE
├── Rapport_Technique_CyberSentinel_2026.pdf # Rapport de conception technique
├── Rapport_CyberSentinel_Complet_modeAvancer.pdf  # Rapport audit mode avancé
├── Rapport_CyberSentinel_Complet-modeSimple.pdf   # Rapport audit mode simple
└── CYBERSENTINEL_EtudesdeMarches.pdf        # Étude de marché
```

**Ports exposés :**

| Service | Port | Protocole |
|---|---|---|
| Flask Frontend | 5000 | HTTP |
| Shuffle SOAR | 3443 | HTTPS |
| Dummy Site (lab) | 8443 | HTTPS |
| Wordlist HTTP Server | 8888 | HTTP |

---

## 5. Structure détaillée des fichiers

### `/frontend_flask/` — Interface utilisateur

```
frontend_flask/
│
├── app.py                        # Application Flask principale
│   │                               - Routes HTTP (/, /audit, /results, /subscribe)
│   │                               - Génération PDF (WeasyPrint)
│   │                               - Envoi email (smtplib / SMTP Gmail)
│   │                               - Scheduler APScheduler (cron 8h00)
│   │                               - Appels webhook vers Shuffle
│   │
├── subscribers.json              # Base des abonnés aux audits automatiques
│   │                               Format : [{"email": "...", "domain": "...", "last_score": ...}]
│   │
├── templates/
│   ├── index.html                # Page d'accueil — formulaire de saisie du domaine
│   ├── dashboard.html            # Tableau de bord des résultats d'audit
│   ├── report_pdf.html           # Template de génération du rapport PDF
│   └── cg-lusion-cards/         # Composant carte interactive (animation CSS)
│       └── ...
│
├── static/
│   ├── css/
│   │   ├── styles.css            # Styles généraux
│   │   ├── index.css             # Styles page d'accueil
│   │   └── dashboard.css         # Styles tableau de bord
│   ├── js/
│   │   ├── script.js             # JavaScript global
│   │   ├── index.js              # Logique page d'accueil
│   │   └── dashboard.js          # Logique tableau de bord (graphiques, scores)
│   └── assets/
│       └── *.png                 # Images de cartes à jouer (UI)
│
└── README.md                     # Documentation du module frontend
```

---

### `/backend_orchestrator/` — Moteur d'audit SOAR

```
backend_orchestrator/
│
├── Moteur_Audit_SAE401.json      # Définition complète du workflow Shuffle
│   │                               - 100+ nœuds d'exécution
│   │                               - Parallélisation dig / Nmap / testssl.sh
│   │                               - Séquençage Nikto → FFUF → OWASP ZAP
│   │                               - Nœuds de délai (anti-DDoS)
│   │                               - Parseurs JSON de normalisation des sorties
│   │
├── README.md                     # Documentation de l'orchestrateur
│
└── Shuffle/                      # Plateforme SOAR Shuffle (open source)
    │
    ├── docker-compose.yml        # Composition Docker de tous les services Shuffle
    ├── .env                      # Variables d'environnement Shuffle
    │
    ├── backend/                  # Moteur Go de Shuffle
    │   ├── Dockerfile
    │   ├── build.sh
    │   └── go-app/
    │       ├── main.go           # Point d'entrée principal (Go)
    │       ├── walkoff.go        # Logique d'exécution des workflows
    │       ├── docker.go         # Intégration Docker pour les apps
    │       ├── main_test.go      # Tests unitaires Go
    │       ├── go.mod            # Dépendances Go
    │       └── app_gen/
    │           └── python-lib/
    │               ├── generator.py      # Génération d'apps Python pour Shuffle
    │               └── requirements.txt
    │
    ├── frontend/                 # Interface d'administration Shuffle (React)
    │   ├── Dockerfile
    │   ├── package.json          # Dépendances Node.js
    │   └── src/
    │       ├── components/       # Composants React réutilisables
    │       ├── views/            # Pages de l'interface admin
    │       ├── css/              # Styles React
    │       └── utils/            # Utilitaires JavaScript
    │
    ├── functions/
    │   ├── onprem/
    │   │   ├── orborus/          # Nœud d'exécution on-premise
    │   │   │   ├── Dockerfile
    │   │   │   └── proxy_server.py
    │   │   └── worker/           # Worker d'exécution des actions
    │   │       └── Dockerfile
    │   └── kubernetes/           # Charts Helm pour déploiement K8s
    │
    └── tests/                    # Suite de tests Shuffle (25+ scripts)
        ├── test_workflow.go
        ├── test_execution.go
        ├── test_files.go
        ├── test_webhooks.go
        └── ...
```

---

### `/dummy_site/` — Environnement de test vulnérable

```
dummy_site/
│
├── app.py                        # Application Flask intentionnellement vulnérable
│   │                               VULNERABILITÉS SIMULÉES (à des fins pédagogiques) :
│   │                               - Faux headers Apache 2.2.14 + PHP 5.3.3 (versions obsolètes)
│   │                               - Absence de headers de sécurité (X-Frame-Options, etc.)
│   │                               - robots.txt révélant /admin_portal, /config.bak, /backup.zip
│   │                               - Endpoint /config.bak exposant de fausses credentials DB
│   │                               - XSS via filtre | safe sur entrée utilisateur
│   │                               - Certificat SSL auto-signé (détectable par testssl.sh)
│   │
├── Dockerfile                    # Image Docker du site vulnérable
├── docker-compose.yml            # Composition Docker (port 8443)
├── requirements.txt              # Dépendances Python (Flask, pyopenssl)
└── README.md                     # Avertissement et documentation du lab
```

> **AVERTISSEMENT** : Ce site est conçu uniquement pour être utilisé comme cible locale dans le cadre de ce projet. Il ne doit jamais être exposé sur un réseau public.

---

### `/docs/` — Documentation

```
docs/
└── README.md                     # Index de la documentation du projet
```

---

### Fichiers racine

| Fichier | Description |
|---|---|
| `start.sh` | Démarre tous les services dans l'ordre : Wordlist Server → Shuffle → Dummy Site → Flask |
| `stop.sh` | Arrête proprement tous les conteneurs Docker et processus |
| `SAE401.pdf` | Cahier des charges officiel de la SAE 401 |
| `Rapport_Technique_CyberSentinel_2026.pdf` | Rapport de conception et d'architecture technique |
| `Rapport_CyberSentinel_Complet_modeAvancer.pdf` | Rapport d'audit complet — Mode Avancé |
| `Rapport_CyberSentinel_Complet-modeSimple.pdf` | Rapport d'audit complet — Mode Simple |
| `CYBERSENTINEL_EtudesdeMarches.pdf` | Étude de marché CyberSentinel |
| `Status parseur ANSSI.txt` | Notes de suivi sur le développement du parseur ANSSI |

---

## 6. Installation et lancement

### Prérequis

- Docker & Docker Compose installés
- Python 3.10+ avec `pip`
- Git

### Étape 1 — Cloner le dépôt

```bash
git clone https://github.com/Cravilly-Olwen/SAE401.git
cd SAE401
git checkout Jeremy
```

### Étape 2 — Démarrer tous les services

```bash
chmod +x start.sh stop.sh
./start.sh
```

Le script `start.sh` lance automatiquement dans l'ordre :
1. **Serveur HTTP wordlists** (port 8888) — listes de mots pour FFUF
2. **Shuffle SOAR** (port 3443) — orchestrateur d'audit
3. **Dummy Site** (port 8443) — cible de test vulnérable
4. **Flask Frontend** (port 5000) — interface utilisateur

### Étape 3 — Accéder à l'application

| Interface | URL |
|---|---|
| Application CyberSentinel | http://localhost:5000 |
| Interface admin Shuffle | https://localhost:3443 |
| Site de test vulnérable | https://localhost:8443 |

### Étape 4 — Importer le workflow Shuffle

1. Ouvrir https://localhost:3443
2. Aller dans **Workflows** > **Import**
3. Importer le fichier `backend_orchestrator/Moteur_Audit_SAE401.json`

### Arrêt des services

```bash
./stop.sh
```

---

## 7. Système de scoring ANSSI

CyberSentinel traduit les résultats techniques en **langage automobile** basé sur la matrice ANSSI :

| Catégorie | Métaphore | Sévérité | Exemple |
|---|---|---|---|
| Critique | Freins coupés | Danger imminent | SQLi, fuite de credentials |
| Majeur | Pneus lisses | Risque élevé | Certificat SSL obsolète, port critique ouvert |
| Important | Anomalie carrosserie | Risque modéré | Version logicielle exposée |
| Mineur | Entretien à prévoir | Risque faible | Header de sécurité manquant |
| Quick Wins | Changement d'ampoule | Correction < 5 min | Ajout d'un header HTTP |

**Score global (sur 100) :**

| Note | Score | Couleur | Signification |
|---|---|---|---|
| A | 90–100 | Vert | Contrôle technique favorable |
| B | 75–89 | Bleu | Quelques points à corriger |
| C | 60–74 | Jaune | Contre-visite recommandée |
| D | 40–59 | Orange | Contre-visite obligatoire |
| F | < 40 | Rouge | Immobilisation |

---

## 8. Environnement de test

Le dossier `dummy_site/` contient un site Flask **volontairement vulnérable** servant de laboratoire pour valider chaque outil d'audit intégré.

**Vulnérabilités simulées :**
- Headers HTTP trompeurs (Apache 2.2.14, PHP 5.3.3)
- Absence de headers de sécurité
- Fichiers sensibles indexés dans `robots.txt`
- Endpoint exposant de fausses credentials base de données
- Faille XSS via rendu non échappé
- Certificat SSL auto-signé

> Cet environnement doit rester **strictement local**. Il n'est pas conçu pour être exposé sur un réseau public.

---

## 9. Documentation et livrables

Tous les documents livrables sont disponibles à la racine du dépôt :

| Document | Contenu |
|---|---|
| `SAE401.pdf` | Cahier des charges et contraintes du projet |
| `Rapport_Technique_CyberSentinel_2026.pdf` | Architecture technique complète, choix de conception |
| `Rapport_CyberSentinel_Complet_modeAvancer.pdf` | Résultats et analyse d'un audit en Mode Avancé |
| `Rapport_CyberSentinel_Complet-modeSimple.pdf` | Résultats et analyse d'un audit en Mode Simple |
| `CYBERSENTINEL_EtudesdeMarches.pdf` | Positionnement marché et analyse concurrentielle |

---

*Projet réalisé dans le cadre de la SAE 401 — BUT Réseaux & Télécommunications 2025–2026.*
