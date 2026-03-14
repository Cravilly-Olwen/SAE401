

&#x20;██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗

██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║

██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║

██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║

╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗

&#x20;╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝


🛡️ Plateforme d'Audit de Sécurité Web Automatisé (SaaS)
Le contrôle technique de votre site internet, pour démocratiser la sécurité web.



📋 Table des matières

Vue d'ensemble \& Fonctionnalités

* Architecture \& Flux de données
* Prérequis
* Installation
* Utilisation
* Surveillance Continue (Cron)
* Scoring ANSSI \& Contrôle Technique
* Dépannage



🔍 Vue d'ensemble \& Fonctionnalités

CyberSentinel est une plateforme SaaS réalisée dans le cadre de la SAE 401. Son but est de démocratiser la cybersécurité. Elle orchestre 6 outils open-source en parallèle et traduit leurs résultats bruts en un rapport vulgarisé, inspiré du modèle WooRank.



✨ Fonctionnalités Principales

* 🌍 Audit à 360° : Analyse du nom de domaine, de l'hébergement serveur et de la couche applicative web.
* ⚙️ Double Mode d'Exécution :

&#x09;Mode Simple : Scan rapide de surface (dig, nmap, nikto).

&#x09;Mode Avancé : Analyse profonde (Fuzzing via ffuf, robustesse via testssl, DAST via OWASP ZAP).

* 🚗 Moteur de Vulgarisation (Le Contrôle Technique) : Traduction des données techniques en alertes claires (Freins coupés, Pneus lisses...).
* 📄 Rapports Automatisés : Génération du rapport au format PDF et envoi direct par Email.
* ⏰ Surveillance Continue : Audit quotidien automatisé avec alerte par mail.



🗂️ Architecture \& Flux de données

┌─────────────────────────────────────────────────────────────────┐

│                      CYBERSENTINEL                              │

│                                                                 │

│   \[Utilisateur]  ──►  \[Flask :5000]  ──►  \[Shuffle SOAR]       │

│                             │                    │              │

│                             │         ┌──────────▼──────────┐  │

│                             │         │  dig   │   nmap      │  │

│                             │         │  nikto │   ffuf      │  │

│                             │         │ testssl│  OWASP ZAP  │  │

│                             │         └──────────┬──────────┘  │

│                             │                    │              │

│                    \[Dashboard]  ◄──  \[Parseur ANSSI Python]     │

│                    \[PDF / Email]                                 │

└─────────────────────────────────────────────────────────────────┘



Arborescence du dépôt :

SAE401/

│

├── 📁 frontend\_flask/              → Interface web \& API

│   ├── app.py                      → Serveur Flask principal

│   ├── templates/

│   │   ├── index.html              → Formulaire d'audit

│   │   ├── dashboard.html          → Tableau de bord résultats

│   │   └── report\_pdf.html         → Template rapport PDF

│   └── static/

│       ├── css/                    → Styles

│       └── js/                     → Scripts frontend

│

├── 📁 backend\_orchestrator/        → Moteur SOAR

│   └── Moteur\_Audit\_SAE401.json    → Workflow Shuffle (à importer)

│

└── 📁 dummy\_site/                  → Laboratoire de test

&#x20;   ├── app.py                      → Site Flask avec failles intentionnelles

&#x20;   ├── Dockerfile

&#x20;   ├── docker-compose.yml

&#x20;   └── requirements.txt



✅ Prérequis

Composant,Version minimale,Vérification

OS,Ubuntu 22.04 / Debian 12 / WSL2,uname -a

Python,3.10+,python3 --version

Docker,24.0+,docker --version

Docker Compose,v2.0+,docker compose version

RAM disponible,4 Go (8 Go recommandés),free -h

Ports libres,"3443, 5000, 8080, 8443, 2222",ss -tlnp



🚀 Installation

1 · Cloner le projet

git clone \[https://github.com/Cravilly-Olwen/SAE401.git](https://github.com/Cravilly-Olwen/SAE401.git)

cd SAE401

git checkout Jeremy



2 · Installer Docker

&#x09;⏭️ Passez cette étape si Docker est déjà installé.



\# Téléchargement et installation automatique

curl -fsSL \[https://get.docker.com](https://get.docker.com) -o get-docker.sh

sudo sh get-docker.sh



\# Ajouter votre utilisateur au groupe docker

sudo usermod -aG docker $USER

newgrp docker



\# Vérification

docker --version

docker compose version



3 · Lancer Shuffle (Orchestrateur)

Shuffle est le cerveau de la plateforme. Il exécute et parallélise tous les outils d'audit.



\# Cloner Shuffle dans /opt

git clone \[https://github.com/Shuffle/Shuffle.git](https://github.com/Shuffle/Shuffle.git) /opt/shuffle

cd /opt/shuffle



\# Démarrer tous les conteneurs Shuffle

docker compose up -d



\# Attendre que les services soient prêts (\~60 secondes)

echo "Attente du démarrage de Shuffle..."

sleep 60

docker ps | grep shuffle



&#x09;🌐 Interface Shuffle : https://localhost:3443

&#x09;⚠️ Ignorez l'avertissement SSL (certificat auto-signé) et créez un compte administrateur à la première connexion.



Vérifier que les réseaux Docker Shuffle existent :

docker network ls | grep shuffle



Vous devez voir deux lignes (shuffle\_shuffle et shuffle\_swarm\_executions). S'ils sont absents, créez-les manuellement :

docker network create shuffle\_shuffle

docker network create shuffle\_swarm\_executions



4 · Importer le workflow d'audit

&#x09;1. Connectez-vous sur https://localhost:3443

&#x09;2. Allez dans Workflows dans le menu

&#x09;3. Cliquez sur le bouton Import (icône ☁️)

&#x09;4. Sélectionnez le fichier : backend\_orchestrator/Moteur\_Audit\_SAE401.json

&#x09;5. Le workflow Moteur\_Audit\_SAE401 apparaît dans votre liste ✅



📌 Récupérer l'URL du Webhook :

Ouvrez le workflow et cliquez sur le bloc Reception\_Commande\_Flask (trigger Webhook). Copiez l'URL affichée (elle ressemble à https://127.0.0.1:3443/api/v1/hooks/webhook\_ID). Gardez cette URL pour l'étape 6.



📌 Mettre à jour l'IP Flask dans Shuffle :

Dans le workflow, ouvrez le bloc Envoi\_Flask et mettez à jour l'URL avec l'IP réelle de votre machine sur le réseau (pas 127.0.0.1) :

http://VOTRE\_IP\_LOCALE:5000/api/report



5 · Démarrer le site vulnérable (lab)

Ce site simule une cible réelle avec des failles intentionnelles pour tester la plateforme.

Faille,Description,Outil détecteur

Header Server: Apache/2.2.14,Version obsolète exposée,Nikto

Fichier /config.bak public,Fuite de credentials BDD,FFUF

/robots.txt révèle dossiers,Information disclosure,Nikto

Certificat SSL auto-signé,TLS invalide,TestSSL

Port SSH 22 ouvert,Service sensible exposé,Nmap

Paramètre ?q= non échappé,XSS potentiel,OWASP ZAP



cd dummy\_site

docker compose up -d --build



Services disponibles après démarrage :

* Site HTTPS vulnérable : https://127.0.0.1:8443
* OWASP ZAP : http://127.0.0.1:8080
* SSH exposé : ssh root@127.0.0.1 -p 2222 (Mot de passe : cyber2026)



6 · Installer et configurer Flask

6.1 — Dépendances système \& virtuelles

sudo apt update \&\& sudo apt install -y \\

&#x20;   python3 python3-pip python3-venv \\

&#x20;   libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \\

&#x20;   libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \\

&#x20;   libcairo2 libgtk-3-0



cd frontend\_flask

python3 -m venv venv

source venv/bin/activate

pip install flask==3.0.0 werkzeug==3.0.0 weasyprint requests urllib3



6.2 — Configurer l'application

Ouvrez frontend\_flask/app.py et :

&#x09;1. Remplacez la ligne \~47 avec l'URL de votre webhook Shuffle copiée à l'étape 4.

&#x09;2. (Optionnel) Modifiez les lignes \~130 avec vos identifiants d'application Gmail pour activer l'envoi d'email.



7 · Démarrer CyberSentinel

cd frontend\_flask

source venv/bin/activate

python app.py



&#x09;🌐 CyberSentinel est disponible sur : http://localhost:5000



🎯 Utilisation

1. Ouvrez http://localhost:5000

2\. Saisissez l'URL cible (ex: https://127.0.0.1:8443)

3\. Choisissez le mode (Simple : \~2 min | Avancé : \~8 min)

4\. Lancez l'audit et patientez jusqu'à l'affichage du Dashboard.



Exporter le rapport :

* 📥 Télécharger PDF : Rapport complet et détaillé au format PDF.
* 📧 Envoyer par email : Envoi du PDF à l'adresse saisie.



⏰ Surveillance Continue (Cron)

Pour activer l'audit quotidien automatisé (scan tous les matins à 8h00 avec envoi par mail) :

1. Ouvrez votre crontab : crontab -e

2\. Ajoutez cette ligne à la fin du fichier (adaptez l'URL et l'email) :

0 8 \* \* \* curl -X POST http://localhost:5000/api/audit -d "url=\[https://votre-site.com](https://votre-site.com)" -d "mode=simple" -d "email=votre.email@domaine.com"



📊 Scoring ANSSI \& Contrôle Technique

Le scoring est calculé selon la matrice Impact × Difficulté d'exploitation de l'ANSSI :

&#x09;			Difficulté d'exploitation →

&#x20;               ┌──────────┬──────────┬──────────┬──────────┐

&#x20;               │Très diff.│ Difficile│ Modérée  │  Facile  │

&#x20; ┌─────────────┼──────────┼──────────┼──────────┼──────────┤

↓ │   Mineur    │  Mineur  │  Mineur  │Important │  Majeur  │

I ├─────────────┼──────────┼──────────┼──────────┼──────────┤

m │   Important │  Mineur  │Important │Important │  Majeur  │

p ├─────────────┼──────────┼──────────┼──────────┼──────────┤

a │   Majeur    │Important │  Majeur  │  Majeur  │ CRITIQUE │

c ├─────────────┼──────────┼──────────┼──────────┼──────────┤

t │   Critique  │Important │  Majeur  │ CRITIQUE │ CRITIQUE │

&#x20; └─────────────┴──────────┴──────────┴──────────┴──────────┘



Le Contrôle Technique Automobile

La restitution technique est traduite via une métaphore automobile pour une compréhension immédiate.

Calcul du score global : Score = 100 − (Critique × 25) − (Majeur × 15) − (Important × 5) − (Mineur × 1)



Catégorie Technique,Métaphore Automobile,Impact \& Signification

Vignette Globale,"Grade A, B, C, D ou F",Score global (Favorable / Contre-visite / Immobilisation).

Critique,🚨 Freins Coupés,"Danger imminent (ex: Faille SQLi, vol de données). Urgence absolue."

Majeur,🛞 Pneus Lisses,"Risque de sortie de route (ex: Certificat SSL obsolète, service exposé)."

Mineur,🚗 Anomalie Carrosserie,"Défaut d'entretien (ex: Headers manquants, fuite d'info basique)."

Info / Basique,💡 Changement d'ampoule,Quick Wins : corrections rapides de 5 minutes.



🔧 Dépannage

<details>

<summary>❌ Le dashboard n'apparaît jamais après l'audit</summary>

Cause probable : Shuffle ne peut pas envoyer le rapport à Flask.

Vérifiez l'IP dans le bloc Envoi\_Flask du workflow Shuffle. Elle doit être celle de votre machine sur le réseau local (pas localhost ni 127.0.0.1).

Vérifiez que Shuffle tourne : docker ps | grep shuffle

</details>



<details>

<summary>❌ Erreur WeasyPrint / génération PDF échoue</summary>

\# Réinstaller les dépendances système

sudo apt install -y --reinstall libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2



\# Tester WeasyPrint

python3 -c "import weasyprint; print('WeasyPrint OK')"

</details>



<details>

<summary>❌ OWASP ZAP ne retourne pas de résultats</summary>

ZAP peut être lent à initialiser. Attendez 30 secondes après le docker compose up, puis si ZAP ne répond toujours pas, forcez le redémarrage :

docker restart zap-server

</details>



<details>

<summary>❌ Erreur "Port already in use"</summary>

\# Identifier quel processus utilise le port (ex: 5000)

sudo lsof -i :5000



\# Tuer le processus bloquant

sudo kill -9 <PID>

</details>



🔒 Charte éthique — Mode White Hat

⚠️ CyberSentinel est un outil d'audit défensif uniquement.

&#x09;✅ Aucune exploitation — observation passive uniquement.

&#x09;✅ Temporisation intégrée dans tous les scans (pas de DDoS involontaire).

&#x09;✅ 100% open-source, aucune dépendance propriétaire.

&#x09;❌ N'utilisez jamais cet outil sur une cible sans autorisation écrite explicite.



L'utilisation de CyberSentinel sur des systèmes tiers sans permission est illégale (Code pénal français, Art. 323-1).



👥 Équipe

Projet SAE 401 — BUT Informatique 2025/2026

Encadrant : Christian Delettre, PhD

Fondateur \& CEO de </DelTekZen> — Expert en transformation digitale



<div align="center">

<i>Made with ❤️ and way too much caffeine ☕</i>

</div>



