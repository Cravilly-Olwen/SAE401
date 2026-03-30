# CyberSentinel

**Plateforme SaaS d'audit de cybersécurité automatisé — SAE 401**
BUT Réseaux & Télécommunications | 2025–2026

CyberSentinel orchestre six outils de sécurité professionnels et restitue les résultats sous la forme d'un **tableau de bord interactif à thème jeu de cartes**. Chaque vulnérabilité détectée devient une carte à jouer à retourner. L'interface, appelée **"Le Tirage"**, s'inspire du vocabulaire du casino pour vulgariser les résultats techniques auprès de non-experts.

---

## Sommaire

1. [Concept et thème](#1-concept-et-thème)
2. [Fonctionnalités](#2-fonctionnalités)
3. [Stack technique](#3-stack-technique)
4. [Architecture du dépôt](#4-architecture-du-dépôt)
5. [Détail de chaque module](#5-détail-de-chaque-module)
6. [Lancement du projet](#6-lancement-du-projet)
7. [Système de scoring — La Main](#7-système-de-scoring--la-main)
8. [Livrables et documents](#8-livrables-et-documents)

---

## 1. Concept et thème

L'interface de résultats s'appelle **"Votre Tirage"**. Les résultats d'audit sont présentés comme une main de cartes à jouer à retourner.

### Les familles (suits) → catégories de vulnérabilités

| Famille | Outil(s) associé(s) | Type de failles couvertes |
|---|---|---|
| **Pique** | FFUF, OWASP ZAP | Fuites de données, vulnérabilités critiques (SQLi, XSS…) |
| **Trèfle** | Nmap | Portes d'accès ouvertes, services réseau exposés |
| **Carreau** | Nikto, TestSSL | Défauts de configuration serveur, TLS faible |
| **Cœur** | Dig | Hygiène web, fuites d'informations mineures (DNS) |

### Les valeurs des cartes → niveaux de sévérité

| Carte | Sévérité | Nom Casino | Description |
|---|---|---|---|
| **As** | Critique | Banqueroute | Faille fatale, exploitation immédiate possible |
| **Roi** | Majeur | Pari Risqué | Danger sérieux, défenses menacées |
| **Valet** | Important | Coup de Bluff | Faiblesse visible de l'extérieur |
| **8** | Mineur | Petite Fuite | Petits réglages d'hygiène à effectuer |

### La Roulette du Risque

La page de résultats contient une **roulette de casino animée** qui visualise la répartition des risques détectés par catégorie (Banqueroute / Pari Risqué / Coup de Bluff / Petite Fuite).

---

## 2. Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Audit 360° | Analyse DNS, ports réseau, TLS/HTTPS, configuration serveur, fuzzing web, DAST applicatif |
| Mode Simple | Scan rapide : dig, Nmap, testssl.sh |
| Mode Avancé | Analyse complète : + Nikto, FFUF, OWASP ZAP |
| Le Tirage | Dashboard interactif — chaque vulnérabilité est une carte à retourner |
| La Roulette du Risque | Roue de casino animée affichant la répartition des risques |
| Rapport PDF | Génération d'un rapport complet A4 téléchargeable |
| Envoi par e-mail | Rapport envoyé directement en pièce jointe par SMTP Gmail |
| Surveillance automatique | Abonnement à des audits planifiés (fréquence + heure configurables) |
| Alerte | Notification par mail si de nouvelles failles sont détectées |
| White Hat | Temporisation intégrée entre FFUF et ZAP pour éviter tout DDoS involontaire |

---

## 3. Stack technique

### Frontend — Interface utilisateur

| Technologie | Rôle |
|---|---|
| Python 3 + Flask | Serveur web, routing, logique métier |
| Jinja2 | Rendu des templates HTML |
| Tailwind CSS | Styles de l'interface |
| JavaScript vanilla | Animations, retournement des cartes, roulette, polling scan |
| GSAP + ScrollTrigger | Animations de défilement du dashboard |
| Lenis | Smooth scroll |
| WeasyPrint | Génération PDF côté serveur |
| APScheduler | Scheduler des audits automatiques |
| smtplib | Envoi des rapports par e-mail (Gmail SMTP) |

### Backend — Orchestration et moteur d'audit

| Technologie | Rôle |
|---|---|
| Shuffle (SOAR) | Orchestrateur de workflows d'audit open source |
| Go (Golang) | Moteur interne de Shuffle |
| OpenSearch | Base de données des workflows et résultats |
| React.js | Interface d'administration Shuffle |
| Docker + Docker Compose | Conteneurisation de tous les services |

### Outils d'audit intégrés

| Outil | Phase | Famille de cartes |
|---|---|---|
| `dig` | Reconnaissance DNS | Cœur |
| `Nmap` | Scan de ports et services | Trèfle |
| `testssl.sh` | Analyse cryptographique TLS/HTTPS | Carreau |
| `Nikto` | Configuration serveur et fichiers exposés | Carreau |
| `FFUF` | Fuzzing de répertoires et fichiers cachés | Pique |
| `OWASP ZAP` | DAST — SQLi, XSS, CSRF | Pique |

---

## 4. Architecture du dépôt

```
SAE401/
│
├── frontend/                            # Interface web Flask — Le Tirage
├── backend/                             # Moteur d'audit Shuffle SOAR
├── lab/                                 # Site vulnérable pour les tests
├── docs/                                # Documentation du projet
│
├── start.sh                             # Démarre tous les services
├── stop.sh                              # Arrête tous les services
├── README.md                            # Ce fichier
│
├── SAE401_Cahier_des_Charges.pdf        # Cahier des charges officiel
├── CyberSentinel_Rapport_Technique_2026.pdf   # Rapport de conception
├── CyberSentinel_Rapport_Mode_Avance.pdf      # Rapport audit mode avancé
├── CyberSentinel_Rapport_Mode_Simple.pdf      # Rapport audit mode simple
└── CyberSentinel_Etude_de_Marche.pdf          # Étude de marché
```

### Ports utilisés

| Service | Port | URL d'accès |
|---|---|---|
| Flask — Interface CyberSentinel | 5000 | http://localhost:5000 |
| Shuffle SOAR | 3443 | https://localhost:3443 |
| Lab (site de test vulnérable) | 8443 | https://127.0.0.1:8443 |
| OWASP ZAP (proxy interne) | 8080 | Interne Docker |
| Serveur de wordlists FFUF | 8888 | Interne |

---

## 5. Détail de chaque module

### `frontend/` — Interface utilisateur (Flask)

```
frontend/
│
├── app.py                        # Application Flask principale
│   │                               Routes exposées :
│   │                                 GET  /                  → Page d'accueil
│   │                                 POST /api/start-scan    → Déclenche l'audit via Shuffle
│   │                                 POST /api/report        → Reçoit les résultats de Shuffle
│   │                                 GET  /dashboard         → Affiche Le Tirage
│   │                                 GET  /api/check-status  → Polling état du scan
│   │                                 GET  /api/download-pdf  → Télécharge le rapport PDF
│   │                                 POST /api/send-email    → Envoie le rapport par mail
│   │                                 POST /api/subscribe     → Abonnement surveillance auto
│   │                                 POST /api/unsubscribe   → Désabonnement
│   │
├── subscribers.json              # Abonnés aux audits automatiques
│                                   Format : [{ email, target, frequency, hour }]
│
├── templates/
│   ├── index.html                # Page d'accueil — saisie de la cible et choix du mode
│   ├── dashboard.html            # "Le Tirage" — cartes + Roulette du Risque
│   │                               + modal surveillance automatique + barre d'actions
│   └── report_pdf.html           # Template du rapport PDF généré par WeasyPrint
│
└── static/
    ├── css/
    │   ├── styles.css            # Styles globaux
    │   ├── index.css             # Styles page d'accueil
    │   └── dashboard.css         # Styles dashboard (cartes, animations, roulette)
    ├── js/
    │   ├── script.js             # JavaScript global
    │   ├── index.js              # Polling du scan, barre de progression
    │   └── dashboard.js          # Retournement cartes, roulette animée, envoi mail
    └── assets/                   # Images des cartes à jouer
        ├── card-front.png        # Dos de carte générique
        ├── dos_pique.png         # Dos — famille Pique
        ├── dos_trefle.png        # Dos — famille Trèfle
        ├── dos_carreau.png       # Dos — famille Carreau
        ├── dos_coeur.png         # Dos — famille Cœur
        ├── as_de_pique.png       # As de Pique   (Critique / Banqueroute)
        ├── as_de_trefle.png      # As de Trèfle  (Critique / Banqueroute)
        ├── roi_de_pique.png      # Roi de Pique  (Majeur / Pari Risqué)
        ├── roi_de_carreau.png    # Roi de Carreau (Majeur / Pari Risqué)
        ├── valet_de_pique.png    # Valet de Pique  (Important / Coup de Bluff)
        ├── valet_de_trefle.png   # Valet de Trèfle (Important / Coup de Bluff)
        ├── 8_de_coeur.png        # 8 de Cœur    (Mineur / Petite Fuite)
        ├── 8_de_carreau.png      # 8 de Carreau (Mineur / Petite Fuite)
        ├── 8_de_trefle.png       # 8 de Trèfle  (Mineur / Petite Fuite)
        └── 7_de_coeur.png        # 7 de Cœur    (Mineur / Petite Fuite)
```

---

### `backend/` — Moteur d'audit SOAR

```
backend/
│
├── audit_workflow.json           # Workflow Shuffle complet (100+ nœuds)
│   │                               Phase 1 — Reconnaissance (exécution parallèle) :
│   │                                 dig, Nmap, testssl.sh
│   │                               Phase 2 — Vulnérabilités (exécution séquentielle) :
│   │                                 Nikto → FFUF → [délai anti-DDoS] → OWASP ZAP
│   │                               Parseurs JSON normalisant les sorties CLI brutes
│   │                               Callback final vers POST /api/report sur Flask
│   │
├── README.md                     # Documentation du module
│
└── Shuffle/                      # Plateforme SOAR Shuffle (open source)
    ├── docker-compose.yml        # Composition Docker des services Shuffle
    ├── .env                      # Variables d'environnement Shuffle
    │
    ├── backend/                  # Moteur Go de Shuffle
    │   ├── Dockerfile
    │   └── go-app/
    │       ├── main.go           # Point d'entrée Go
    │       ├── walkoff.go        # Exécution des workflows
    │       ├── docker.go         # Intégration Docker
    │       ├── main_test.go      # Tests Go
    │       ├── go.mod / go.sum   # Dépendances Go
    │       └── app_gen/
    │           └── python-lib/
    │               ├── generator.py       # Génération d'apps Python pour Shuffle
    │               └── requirements.txt
    │
    ├── frontend/                 # Interface d'administration Shuffle (React)
    │   ├── Dockerfile
    │   ├── package.json
    │   └── src/
    │       ├── components/       # Composants React
    │       ├── views/            # Pages de l'interface admin
    │       └── utils/
    │
    ├── functions/
    │   └── onprem/
    │       ├── orborus/          # Nœud d'exécution on-premise
    │       └── worker/           # Worker Docker des actions
    │
    └── tests/                    # Tests Shuffle (25+ scripts)
```

---

### `lab/` — Laboratoire de test vulnérable

```
lab/
│
├── app.py                        # Site Flask intentionnellement vulnérable
│   │                               Vulnérabilités simulées à des fins pédagogiques :
│   │                                 - Faux headers Apache 2.2.14 + PHP 5.3.3
│   │                                 - Headers de sécurité absents
│   │                                 - robots.txt révélant /admin_portal, /config.bak
│   │                                 - Endpoint /config.bak (fausses credentials DB)
│   │                                 - XSS via filtre Jinja2 | safe non échappé
│   │                                 - Certificat SSL auto-signé
│   │
├── Dockerfile                    # Image Docker du site de test
├── docker-compose.yml            # Réseau isolé + OWASP ZAP intégré (port 8443)
└── requirements.txt              # Flask, pyopenssl
```

> Ce site ne doit être utilisé qu'en local. Il ne doit jamais être exposé sur un réseau public.

---

### `docs/`

```
docs/
└── README.md                     # Index de la documentation
```

---

## 6. Lancement du projet

### Prérequis

- Docker et Docker Compose installés et démarrés
- Python 3.10+ avec pip
- Dépendances Python :

```bash
pip install flask requests weasyprint apscheduler urllib3
```

### Démarrer tous les services

```bash
chmod +x start.sh
./start.sh
```

Le script `start.sh` lance automatiquement dans l'ordre :

1. **Serveur de wordlists** (port 8888) — listes de mots pour FFUF
2. **Shuffle SOAR** (port 3443) — attend la disponibilité avant de continuer
3. **Lab + OWASP ZAP** (port 8443) — environnement de test vulnérable
4. **Flask CyberSentinel** (port 5000) — au premier plan, logs visibles en direct

`Ctrl+C` arrête proprement tous les services.

### Importer le workflow dans Shuffle

1. Ouvrir https://localhost:3443
2. Aller dans **Workflows** → **Import**
3. Sélectionner `backend/audit_workflow.json`

### Accéder à l'application

| Interface | URL |
|---|---|
| CyberSentinel — Le Tirage | http://localhost:5000 |
| Admin Shuffle | https://localhost:3443 |
| Lab — Site de test vulnérable | https://127.0.0.1:8443 |

---

## 7. Système de scoring — La Main

### Calcul du score de robustesse (sur 100)

```
Score = 100 − (Critique × 25) − (Majeur × 15) − (Important × 5) − (Mineur × 1)
```

### Notes et signification

| Note | Score | Signification |
|---|---|---|
| **A** | 90 – 100 | Excellent — Situation saine |
| **B** | 70 – 89 | Bon — Quelques ajustements recommandés |
| **C** | 50 – 69 | Moyen — Faiblesses importantes à corriger |
| **D** | 20 – 49 | Dangereux — Intervention rapide nécessaire |
| **F** | < 20 | Critique — Urgence absolue |

### Catégories de risque

| Catégorie casino | Sévérité réelle | Carte associée |
|---|---|---|
| Banqueroute | Critique | As |
| Pari Risqué | Majeur | Roi |
| Coup de Bluff | Important | Valet |
| Petite Fuite | Mineur | 8 |

---

## 8. Livrables et documents

Tous les documents sont disponibles à la racine du dépôt :

| Fichier | Contenu |
|---|---|
| `SAE401_Cahier_des_Charges.pdf` | Cahier des charges officiel de la SAE 401 |
| `CyberSentinel_Rapport_Technique_2026.pdf` | Architecture technique, choix de conception, flux de données |
| `CyberSentinel_Rapport_Mode_Avance.pdf` | Résultats d'un audit complet en Mode Avancé |
| `CyberSentinel_Rapport_Mode_Simple.pdf` | Résultats d'un audit en Mode Simple |
| `CyberSentinel_Etude_de_Marche.pdf` | Analyse de marché et positionnement concurrentiel |

---

*SAE 401 — BUT Réseaux & Télécommunications 2025–2026*
