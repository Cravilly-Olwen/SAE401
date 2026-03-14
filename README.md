Gemini a dit
Voici le fichier README.md complet et prêt à être utilisé. Tu n'as plus qu'à copier le bloc ci-dessous et à le coller dans ton fichier :

Markdown
<div align="center">

```text
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
🛡️ Plateforme d'Audit de Cybersécurité Automatisé (SaaS)
Le contrôle technique de votre site internet, pour démocratiser la sécurité web.

</div>

📖 Présentation du Projet
Ce projet, réalisé dans le cadre de la SAE 401, a pour objectif de démocratiser la cybersécurité pour les non-experts.

La plateforme CyberSentinel orchestre 6 outils d'audit complexes en arrière-plan et restitue les résultats sous la forme d'un tableau de bord vulgarisé reprenant le modèle d'un "Contrôle Technique Automobile" 🚗. Fini le jargon incompréhensible, les rapports techniques sont traduits en alertes claires (inspirées des rapports SEO type WooRank) basées sur les standards de l'ANSSI.

✨ Fonctionnalités Principales
🌍 Audit à 360° : Analyse du nom de domaine, de l'hébergement serveur et de la couche applicative web.

⚙️ Double Mode d'Exécution :

Mode Simple : Scan rapide de surface (Reconnaissance et failles courantes).

Mode Avancé : Analyse profonde et recherche de vulnérabilités critiques (Fuzzing, DAST).

🚗 Moteur de Vulgarisation (Le Contrôle Technique) : Traduction des données techniques brutes en alertes compréhensibles.

📄 Rapports Automatisés : Génération du rapport au format PDF et envoi direct par Email.

⏰ Surveillance Continue : Possibilité de s'abonner à un audit quotidien automatisé (Cron à 8h00) avec alerte par mail.

🛠️ Stack Technique & Outils Exclusifs
CyberSentinel s'appuie sur une architecture moderne et orchestre 6 outils de sécurité open-source de référence :

Frontend / Interface : Python 3 (Flask), HTML/CSS, Jinja2.

Orchestrateur SOAR : Shuffle (via Docker) gérant la parallélisation et l'asynchronisme.

Les Outils d'Audit Intégrés :

dig : Reconnaissance DNS et zone.

Nmap : Scan de ports et détection de services/OS.

testssl.sh : Analyse de la robustesse cryptographique (HTTPS/TLS).

FFUF : Fuzzing et découverte de contenus/fichiers cachés.

Nikto : Scan des configurations serveur et des fichiers par défaut dangereux.

OWASP ZAP : Scanner applicatif dynamique (DAST) pour les failles complexes (SQLi, XSS).

📋 Table des matières
Architecture & Flux de données

Prérequis

Installation

Utilisation

Configuration de la Surveillance Continue (Cron)

Scoring ANSSI & Contrôle Technique

Dépannage

Charte Éthique

🗂️ Architecture & Flux de données
Plaintext
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
Structure du dépôt :

🌐 /frontend_flask : Interface web, API, génération PDF et configuration email.

⚙️ /backend_orchestrator : Workflows Shuffle (fichiers JSON à importer), scripts de parsing.

🎯 /dummy_site : Environnement de test local vulnérable (laboratoire de démonstration).

📚 /docs : Cahier des charges, architecture détaillée, matrice Excel ANSSI.

✅ Prérequis
Composant	Version minimale	Vérification
OS	Ubuntu 22.04 / Debian 12 / WSL2	uname -a
Python	3.10+	python3 --version
Docker	24.0+	docker --version
Docker Compose	v2.0+	docker compose version
RAM	4 Go (8 Go recommandés)	free -h
Ports libres	3443, 5000, 8080, 8443, 2222	ss -tlnp
🚀 Installation
1 · Cloner le projet
Bash
git clone [https://github.com/Cravilly-Olwen/SAE401.git](https://github.com/Cravilly-Olwen/SAE401.git)
cd SAE401
git checkout Jeremy
2 · Installer Docker
⏭️ Passez cette étape si Docker est déjà installé.

Bash
curl -fsSL [https://get.docker.com](https://get.docker.com) -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
3 · Lancer Shuffle (Orchestrateur)
Bash
git clone [https://github.com/Shuffle/Shuffle.git](https://github.com/Shuffle/Shuffle.git) /opt/shuffle
cd /opt/shuffle
docker compose up -d
sleep 60 # Attente du démarrage
🌐 Interface Shuffle : https://localhost:3443 (Créez un compte admin, ignorez l'alerte SSL).

Vérifiez que les réseaux Docker Shuffle existent :

Bash
docker network ls | grep shuffle
# Si absent :
# docker network create shuffle_shuffle
# docker network create shuffle_swarm_executions
4 · Importer le workflow d'audit
Connectez-vous sur https://localhost:3443

Allez dans Workflows > Import (icône ☁️)

Sélectionnez le fichier : backend_orchestrator/Moteur_Audit_SAE401.json

Important : Récupérez l'URL du Webhook dans le bloc Reception_Commande_Flask (ex: https://127.0.0.1:3443/api/v1/hooks/webhook_ID).

Important : Mettez à jour l'IP Flask dans le bloc Envoi_Flask avec l'IP réelle de votre machine sur le réseau local (ex: http://192.168.1.42:5000/api/report).

5 · Démarrer le site vulnérable (Lab)
Ce site simule une cible avec des failles intentionnelles (certificat invalide, port SSH exposé, XSS...).

Bash
cd dummy_site
docker compose up -d --build
Le site sera accessible sur https://127.0.0.1:8443.

6 · Installer et configurer Flask
Bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info libcairo2 libgtk-3-0

cd frontend_flask
python3 -m venv venv
source venv/bin/activate
pip install flask==3.0.0 werkzeug==3.0.0 weasyprint requests urllib3
Ouvrez frontend_flask/app.py et modifiez :

Ligne ~47 : Insérez l'URL de votre Webhook Shuffle.

Lignes ~130 : Configurez vos identifiants d'application Gmail (optionnel, pour l'envoi de PDF).

7 · Démarrer CyberSentinel
Bash
python app.py
🌐 CyberSentinel est disponible sur : http://localhost:5000

🎯 Utilisation
Ouvrez http://localhost:5000

Saisissez l'URL cible (ex: https://127.0.0.1:8443)

Choisissez le mode (Simple : ~2 min | Avancé : ~8 min)

Lancez l'audit et patientez jusqu'à l'affichage du Dashboard.

⏰ Configuration de la Surveillance Continue (Cron)
Pour activer la fonctionnalité d'audit quotidien automatisé (qui lance un scan tous les matins à 8h00 et vous l'envoie par mail), vous pouvez utiliser le planificateur de tâches Linux (cron).

Ouvrez votre crontab :

Bash
crontab -e
Ajoutez la ligne suivante à la fin du fichier (en remplaçant par l'URL cible et votre adresse mail) :

Bash
0 8 * * * curl -X POST http://localhost:5000/api/audit -d "url=[https://votre-site.com](https://votre-site.com)" -d "mode=simple" -d "email=votre.email@domaine.com"
L'audit se lancera désormais de manière autonome tous les jours à 8h00 précises.

📊 Scoring ANSSI & Contrôle Technique
La traduction technique vers la vulgarisation s'appuie sur la matrice Impact × Difficulté d'exploitation de l'ANSSI.

Calcul du score global : Score = 100 − (Critique × 25) − (Majeur × 15) − (Important × 5) − (Mineur × 1)

Catégorie Technique	Métaphore Automobile	Impact & Signification
Vignette Globale	A, B, C, D ou F	Score de sécurité (Favorable / Contre-visite / Immobilisation).
Critique	🚨 Freins Coupés	Danger imminent (ex: Faille SQLi, vol de données). Urgence absolue.
Majeur	🛞 Pneus Lisses	Risque de sortie de route (ex: Certificat SSL obsolète, service exposé).
Mineur	🚗 Anomalie Carrosserie	Défaut d'entretien (ex: Headers manquants, fuite d'info basique).
Info / Basique	💡 Changement d'ampoule	Quick Wins : corrections rapides de 5 minutes.
🔧 Dépannage
Le dashboard n'apparaît jamais : Vérifiez que l'IP dans le bloc Shuffle Envoi_Flask est bien celle de votre machine sur le réseau local (et pas localhost ou 127.0.0.1).

Erreur WeasyPrint (PDF) : Assurez-vous d'avoir bien installé les dépendances système (libcairo2, libpango, etc.) listées à l'étape 6.

OWASP ZAP ne trouve rien : Le conteneur met parfois du temps à démarrer. Attendez 30s ou redémarrez-le avec docker restart zap-server.

Port already in use : Tuez le processus bloquant avec sudo kill -9 $(sudo lsof -t -i:5000).

🔒 Charte Éthique — Mode White Hat
⚠️ CyberSentinel est un outil d'audit défensif uniquement.

✅ Aucune exploitation — observation passive uniquement.

✅ Temporisation intégrée dans tous les scans (pas de DDoS involontaire) pour garantir la disponibilité des services.

✅ 100% open-source, aucune dépendance propriétaire.

❌ N'utilisez jamais cet outil sur une cible sans autorisation écrite explicite.

L'utilisation de CyberSentinel sur des systèmes tiers sans permission est illégale (Code pénal français, Art. 323-1).

👥 Équipe
Projet SAE 401 — BUT Informatique 2025/2026

Encadrant : Christian Delettre, PhD
Fondateur & CEO de </DelTekZen> — Expert en transformation digitale

<div align="center">
<i>Made with ❤️ and way too much caffeine ☕</i>
</div>

